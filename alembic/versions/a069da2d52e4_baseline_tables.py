"""baseline_tables

Revision ID: a069da2d52e4
Revises: 
Create Date: 2020-05-20 00:07:42.597268

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a069da2d52e4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('batches',
    sa.Column('uid', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(length=75), nullable=True),
    sa.Column('sweet_reference', sa.String(length=30), nullable=True),
    sa.Column('weight', sa.Float(precision=2), nullable=True),
    sa.PrimaryKeyConstraint('uid', name=op.f('pk_batches'))
    )
    op.create_table('companies',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('channel', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('uid', name=op.f('pk_companies'))
    )
    op.create_table('expenses',
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('payments', sa.Float(precision=2), nullable=True),
    sa.PrimaryKeyConstraint('date', name=op.f('pk_expenses'))
    )
    op.create_table('ingredients',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('sku', sa.String(length=50), nullable=True),
    sa.Column('name', sa.String(length=150), nullable=True),
    sa.Column('cost_price', sa.Float(precision=2), nullable=True),
    sa.Column('pack_size', sa.Float(precision=2), nullable=True),
    sa.Column('on_hand', sa.Float(precision=5), nullable=True),
    sa.Column('available', sa.Float(precision=5), nullable=True),
    sa.Column('committed', sa.Float(precision=5), nullable=True),
    sa.PrimaryKeyConstraint('uid', name=op.f('pk_ingredients'))
    )
    op.create_table('orders',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('submitted_date', sa.Date(), nullable=True),
    sa.Column('due_date', sa.Date(), nullable=True),
    sa.Column('invoice_date', sa.Date(), nullable=True),
    sa.Column('cost', sa.Float(precision=2), nullable=True),
    sa.Column('shopify', sa.Boolean(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.uid'], name=op.f('fk_orders_company_id_companies')),
    sa.PrimaryKeyConstraint('uid', 'shopify', name=op.f('pk_orders'))
    )
    op.create_table('products',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=True),
    sa.Column('sku', sa.String(length=50), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('price', sa.Float(precision=2), nullable=True),
    sa.Column('batch_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['batch_id'], ['batches.uid'], name=op.f('fk_products_batch_id_batches')),
    sa.PrimaryKeyConstraint('uid', name=op.f('pk_products'))
    )
    op.create_table('recipes',
    sa.Column('quantity', sa.Float(precision=3), nullable=True),
    sa.Column('batch_id', sa.BigInteger(), nullable=False),
    sa.Column('ingredient_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['batch_id'], ['batches.uid'], name=op.f('fk_recipes_batch_id_batches')),
    sa.ForeignKeyConstraint(['ingredient_id'], ['ingredients.uid'], name=op.f('fk_recipes_ingredient_id_ingredients')),
    sa.PrimaryKeyConstraint('batch_id', 'ingredient_id', name=op.f('pk_recipes'))
    )
    op.create_table('orderitems',
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('shopify', sa.Boolean(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['order_id', 'shopify'], ['orders.uid', 'orders.shopify'], name=op.f('fk_orderitems_order_id_orders')),
    sa.ForeignKeyConstraint(['product_id'], ['products.uid'], name=op.f('fk_orderitems_product_id_products')),
    sa.PrimaryKeyConstraint('order_id', 'shopify', 'product_id', name=op.f('pk_orderitems'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orderitems')
    op.drop_table('recipes')
    op.drop_table('products')
    op.drop_table('orders')
    op.drop_table('ingredients')
    op.drop_table('expenses')
    op.drop_table('companies')
    op.drop_table('batches')
    # ### end Alembic commands ###
