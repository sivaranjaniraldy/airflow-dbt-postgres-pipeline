   select
       order_id,
       order_item_id,
       product_id,
       seller_id,
       price::numeric as price,
       freight_value::numeric as freight_value
   from {{ source('raw', 'order_items') }}