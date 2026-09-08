with orders as (
    select * from {{ ref('stg_orders') }}
),

customers as (
    select * from {{ ref('stg_customers') }}
),

payments as (
    select
        order_id,
        sum(payment_value) as total_payment_value,
        count(distinct payment_type) as payment_type_count
    from {{ ref('stg_order_payments') }}
    group by order_id
),

order_items as (
    select
        order_id,
        count(*) as item_count,
        sum(price) as total_item_price,
        sum(freight_value) as total_freight_value
    from {{ ref('stg_order_items') }}
    group by order_id
)

select
    o.order_id,
    o.customer_id,
    c.customer_city,
    c.customer_state,
    o.order_status,
    o.order_purchase_timestamp,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,
    oi.item_count,
    oi.total_item_price,
    oi.total_freight_value,
    p.total_payment_value,
    p.payment_type_count
from orders o
left join customers c on o.customer_id = c.customer_id
left join order_items oi on o.order_id = oi.order_id
left join payments p on o.order_id = p.order_id