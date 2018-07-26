from django.db import models
from datetime import date
# Create your models here.
from django.conf import settings
from django.db import models
from .errors import InsufficientBalance
from django.db import transaction
from services.models import ServiceOrder

# We'll be using BigIntegerField by default instead
# of DecimalField for simplicity. This can be configured
# though by setting `WALLET_CURRENCY_STORE_FIELD` in your
# `settings.py`.
CURRENCY_STORE_FIELD = getattr(settings,
                               'WALLET_CURRENCY_STORE_FIELD', models.DecimalField)


class Wallet(models.Model):
    # We should reference to the AUTH_USER_MODEL so that
    # when this module is used and a different User is used,
    # this would still work out of the box.
    #
    # See 'Referencing the User model' [1]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    # protect in the weird event someone deletes their account with money still there

    # This stores the wallet's current balance. Also acts
    # like a cache to the wallet's balance as well.
    current_balance = models.DecimalField(default=0.00, decimal_places=2, max_digits=7)

    # The date/time of the creation of this wallet.
    created_at = models.DateTimeField(auto_now_add=True)

    def deposit(self, value):
        """Deposits a value to the wallet.
        Also creates a new transaction with the deposit
        value.
        """
        with transaction.atomic():
            self.transaction_set.create(
                value=value,
                running_balance=self.current_balance + value
            )
            self.current_balance += value
            self.save()

    def withdraw(self, value):
        """Withdraw's a value from the wallet.
        Also creates a new transaction with the withdraw
        value.
        Should the withdrawn amount is greater than the
        balance this wallet currently has, it raises an
        :mod:`InsufficientBalance` error. This exception
        inherits from :mod:`django.db.IntegrityError`. So
        that it automatically rolls-back during a
        transaction lifecycle.
        """
        if value > self.current_balance:
            raise InsufficientBalance('This wallet has insufficient balance.')

        with transaction.atomic():
            self.transaction_set.create(
                value=-value,
                running_balance=self.current_balance - value
            )
            self.current_balance -= value
            self.save()

    def transfer(self, wallet, value):
        """Transfers an value to another wallet.
        Uses `deposit` and `withdraw` internally.
        """
        print("[*] Transferring from Wallet")
        with transaction.atomic():
            self.withdraw(value)
            with transaction.atomic():
                wallet.deposit(value)


class Invoice(models.Model):
    paypal = 'p'
    creditcard = 'c'
    bitpay = 'b'
    platform_choices = (
        (paypal, 'PayPal'),
        (bitpay, "BitPay"),
        (creditcard, "Credit Card")
    )
    payment_type = models.CharField(max_length=2, choices=platform_choices, default=bitpay)
    uid = models.TextField()
    order = models.OneToOneField(ServiceOrder, on_delete=models.CASCADE,
                                 default=None, null=True, blank=True)

    def get_bitpay_url(self):
        return "https://test.bitpay.com/invoice?id={0}".format(self.uid)


class Transaction(models.Model):
    # The wallet that holds this transaction.
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT)

    # The value of this transaction.
    value = models.DecimalField(default=0.00, decimal_places=2, max_digits=7)

    # The value of the wallet at the time of this
    # transaction. Useful for displaying transaction
    # history.
    running_balance = models.DecimalField(default=0.00, decimal_places=2, max_digits=7)

    # The date/time of the creation of this transaction.
    created_at = models.DateTimeField(auto_now_add=True)


class EscrowWallet(models.Model):
    from_account = models.ForeignKey(Wallet, related_name='outgoing_payment_holds', on_delete=models.PROTECT)
    target_account = models.ForeignKey(Wallet, related_name='incoming_payment_holds', on_delete=models.PROTECT)
    value = models.DecimalField(decimal_places=2, max_digits=8, default=0)
    created_on = models.DateField(auto_now=True)
    payed_out = models.BooleanField(default=False)
    payed_on = models.DateField(blank=True, default=None, null=True)

    def release_funds(self):
        self.target_account.deposit(self.value)
        self.payed_out = True
        self.payed_on = date.today()
        self.save()

        with transaction.atomic():
            self.from_account.transaction_set.create(
                value=self.value,
                running_balance=self.from_account.current_balance)

    def hold_funds(self, value):
        self.from_account.transfer(self, value)

    def deposit(self, value):
        print("[*] Depositing into Escrow Wallet")
        with transaction.atomic():
            self.value += value
            self.save()

    def __str__(self):
        return "Escrow between {0} and {1}".format(self.from_account, self.target_account)
