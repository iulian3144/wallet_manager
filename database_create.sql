-- Database creation script as used by MyWallet
DROP TABLE IF EXISTS main.tbl_account;
CREATE TABLE tbl_account (
  acc_id integer PRIMARY KEY AUTOINCREMENT,
  acc_name text,
  acc_initial float,
  acc_order integer,
  acc_is_closed integer default 0,
  acc_color text,
  acc_is_credit integer default 0,
  acc_min_limit float
);


DROP TABLE IF EXISTS main.tbl_trans;
CREATE TABLE tbl_trans(
  exp_id integer PRIMARY KEY AUTOINCREMENT,
  exp_amount float,
  exp_cat integer,
  exp_acc_id integer,
  exp_payee_name text,
  exp_date text,
  exp_month text,
  exp_is_debit integer default 0,
  exp_note text,
  exp_is_paid integer default 1,
  exp_is_bill integer default 0,
  exp_remind_val integer default -1,
  exp_notify_date text default null,
  exp_rec_id integer default -1
);

DROP TABLE IF EXISTS main.tbl_r_trans;
CREATE TABLE tbl_r_trans(
  r_exp_id integer PRIMARY KEY AUTOINCREMENT,
  r_exp_amount float,
  r_exp_cat integer,
  r_exp_acc_id integer,
  r_exp_payee_name text,
  r_exp_date text,
  r_exp_is_debit integer default 0,
  r_exp_note text,
  r_exp_remind_val integer default -1,
  r_exp_week_month text default null,
  r_exp_end_date text,
  r_exp_freq integer,
  r_exp_cycle integer
);

CREATE TABLE tbl_cat(
  category_id integer PRIMARY KEY AUTOINCREMENT,
  category_name text,
  category_color text,
  category_is_inc integer,
  category_icon integer
);

DROP TABLE IF EXISTS main.tbl_notes;
CREATE TABLE tbl_notes(
  notey_id integer PRIMARY KEY AUTOINCREMENT,
  note_text text,
  note_payee_payer integer default -1
);

DROP TABLE IF EXISTS main.tbl_transfer;
CREATE TABLE tbl_transfer(
  trans_id integer PRIMARY KEY AUTOINCREMENT,
  trans_from_id integer,
  trans_to_id integer,
  trans_amount float,
  trans_date text,
  trans_note text
);

DROP TABLE IF EXISTS main.tbl_budget;
CREATE TABLE tbl_budget(
  budget_id integer PRIMARY KEY AUTOINCREMENT,
  budget_cat_id integer,
  budget_amount float,
  budget_cycle integer default 1
);
