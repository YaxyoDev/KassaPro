Kassa Pro App

Do'kon savdosini qayd etib, hisob-kitob ishini qilovchi dastur.

Imkoniyatlar:

1) Mahsulotlar
    mahsulot qo'shish
    mahsulot yangilash
    mahsulot ko'rish
    mahsulot o'chirish
2) Savdo qilish
    mahsulot sotish
    savdo tarixi

<====================================================>

Database:

users:

-id             (user id)
-login          (user login, name)
-password       (user password)
-status         (user status, active, inactive)
-joined_at      (user joined date, datetime)

products:

-id             (product id)
-name           (product name)
-barcode        (product barcode, unikal)
-price          (product price, UZS)
-quantity       (product quanty, count)
-status         (product status, active, inactive)
-created_at     (product created date, datetime)

sales:

-id             (sale id)
-sale_owner     (sale user, from users)
-saled_items    (saled items, name list)
-total_sum      (saled items total sum, UZS)
-paid_sum       (client paid sum for saled items)
-discount       (discount for total_sum, %)
-payment        (payment method, cash, card, click)
-saled_at       (sale date, datetime)


<====================================================>

UI

Main UI: =>

    Savdo 
    Savdo tarixi
    Mahsulotlar
    Xodimlar
    Bugungi hisobot
--------------------------------------
Savdo UI: =>

    Search by barcode
    Search by name
    Carts
    Checks
--------------------------------------
Savdo tarixi UI: =>

    Histroy by date
        sales info
            id |  sale_owner | saled_items | total_sum | paid_sum | discount | payment | saled_at
example:    1  |  Yaxyo      | dropdown    | 100,000UZS| 90,000UZS| 10%      | cash    | 02.02.2026:16:30:00
                             | item1 x1
                             | item2 x2
                             | item3 x3
--------------------------------------
Mahsulotlar UI: =>

    Search by name
        products info
            id |  name |  barcode  | price | quantity | created_at          | status | Select
example:    1  |  item | 484486484 | 35000 | 350      | 01.02.2025:01:00:00 | active | 

    delete selected
    
    Mahsulot qo'shish
    Mahsulot yangilash
--------------------------------------
Mahsulot qo'shish UI: =>
    

--------------------------------------
Mahsulot yangilash UI: => 

--------------------------------------
Xodimlar UI: =>

            id |  login |  password | joined_at          | status | Select
example:    1  |  Yaxyo |  1710     | 01.02.2024:10:30:00| active | 

    delete selected

    Xodim qo'shish
--------------------------------------
Xodim qo'shish UI: =>


<====================================================>

File Strukture 

Kassa_Pro
    main.py
    config.py
    /database
        __init__.py
        sqlite3.db
        models.py
        request_user.py
        request_product.py
        request_sale.py
    /ui
        __init__.py
        main_ui.py
        ...
    /tutorial
        README.md
        TASK.md