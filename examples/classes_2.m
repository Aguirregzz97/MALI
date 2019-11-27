class Balance {
  attr {
    public float total;
  }

  init (float initial) {
    total = initial;
  }

  public void deposit(float amount) {
    total = total + amount;
  }

  public void withdrawal(float amount) {
    total = total - amount;
  }
}

class BankAccount {
  attr {
    public Balance balance;
  }

  init(float initial) {
    balance.init(initial);
  }
}

class Customer {
  attr {
    public int customer_id;
    public BankAccount bank_account;
  }

  init(int cid, float initial) {
    customer_id = cid;
    bank_account.init(initial);
  }
}

func float addition(float x1, float x2) {
  return x1 + x2;
}

main {
  var {
    Customer customer1, customer2;
    float val;
  }

  customer1.init(1, 0);
  customer1.bank_account.balance.deposit(1000);
  customer1.bank_account.balance.withdrawal(500);

  customer2.init(2, 0);
  customer2.bank_account.balance.deposit(1000);

  val = addition(addition(250, 250),
                 customer1.bank_account.balance.total);

  write val, '\n';

  customer1.bank_account.balance.total = 0;
  write customer1.bank_account.balance.total, '\n';
}
