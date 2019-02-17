-- this script is used to import data from a sqlite database exported by MyWallet android application
SELECT
  exp_date as Date,
  acc_name as Account,
  category_name as Category,
  exp_note as Note,
  exp_amount as Amount,
  exp_is_debit as Debit
FROM
  tbl_trans, tbl_cat, tbl_account
WHERE
  exp_cat = category_id
  AND exp_acc_id = acc_id
