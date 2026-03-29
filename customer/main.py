import mysql.connector
import csv
import os

# ──────────────────────────────────────────────────────────
#  DATABASE CONNECTION
# ──────────────────────────────────────────────────────────

def get_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",   # your password
        database="customer_trends"
    )
    return conn


# ──────────────────────────────────────────────────────────
#  SETUP DATABASE AND TABLE
# ──────────────────────────────────────────────────────────

def setup_database():
    # First connect without database to create it
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234"       # <-- change this to your MySQL password
    )
    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS customer_trends")
    cursor.execute("USE customer_trends")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS shopping_behavior (
            customer_id        INT PRIMARY KEY,
            age                INT,
            gender             VARCHAR(10),
            item_purchased     VARCHAR(50),
            category           VARCHAR(50),
            purchase_amount    DECIMAL(10,2),
            location           VARCHAR(50),
            size               VARCHAR(5),
            color              VARCHAR(30),
            season             VARCHAR(20),
            review_rating      DECIMAL(3,1),
            subscription       VARCHAR(5),
            shipping_type      VARCHAR(30),
            discount_applied   VARCHAR(5),
            promo_code_used    VARCHAR(5),
            previous_purchases INT,
            payment_method     VARCHAR(30),
            purchase_frequency VARCHAR(30)
        )
    """)

    # Insert sample data
    sample_data = [
        (1, 25, 'Male', 'T-shirt', 'Clothing', 50.00, 'California', 'M', 'Blue', 'Summer', 4.5, 'Yes', 'Standard', 'No', 'No', 2, 'Credit Card', 'Monthly'),
        (2, 30, 'Female', 'Jeans', 'Clothing', 75.00, 'New York', 'L', 'Black', 'Fall', 4.0, 'No', 'Express', 'Yes', 'Yes', 1, 'PayPal', 'Weekly'),
        (3, 22, 'Male', 'Sneakers', 'Footwear', 100.00, 'Texas', '10', 'White', 'Spring', 5.0, 'Yes', 'Free Shipping', 'No', 'No', 3, 'Cash', 'Annually'),
        (4, 35, 'Female', 'Dress', 'Clothing', 120.00, 'Florida', 'S', 'Red', 'Winter', 4.2, 'No', 'Standard', 'Yes', 'Yes', 0, 'Credit Card', 'Quarterly'),
        (5, 28, 'Male', 'Hat', 'Accessories', 25.00, 'Illinois', 'One Size', 'Green', 'Summer', 3.8, 'Yes', 'Express', 'No', 'No', 4, 'Debit Card', 'Bi-Weekly'),
    ]

    cursor.executemany("""
        INSERT IGNORE INTO shopping_behavior VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, sample_data)

    conn.commit()
    print("\nDatabase, table created, and sample data inserted successfully!")
    cursor.close()
    conn.close()


# ──────────────────────────────────────────────────────────
#  1. VIEW ALL CUSTOMERS
# ──────────────────────────────────────────────────────────

def view_all_customers():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT customer_id, age, gender, item_purchased, category,
               purchase_amount, season, subscription
        FROM shopping_behavior
        LIMIT 20
    """)
    rows = cursor.fetchall()

    print("\n--- ALL CUSTOMERS (showing first 20) ---")
    print(f"{'ID':<6} {'Age':<5} {'Gender':<8} {'Item':<20} {'Category':<12} {'Amount':<10} {'Season':<8} {'Sub'}")
    print("-" * 80)
    for row in rows:
        print(f"{row[0]:<6} {row[1]:<5} {row[2]:<8} {row[3]:<20} {row[4]:<12} ${row[5]:<9} {row[6]:<8} {row[7]}")

    cursor.execute("SELECT COUNT(*) FROM shopping_behavior")
    total = cursor.fetchone()[0]
    print(f"\nTotal records in database: {total}")

    cursor.close()
    conn.close()


# ──────────────────────────────────────────────────────────
#  2. SEARCH CUSTOMER BY ID
# ──────────────────────────────────────────────────────────

def search_customer():
    customer_id = input("Enter Customer ID to search: ").strip()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM shopping_behavior WHERE customer_id = %s", (customer_id,))
    row = cursor.fetchone()

    if row:
        print("\n--- CUSTOMER DETAILS ---")
        print(f"Customer ID       : {row[0]}")
        print(f"Age               : {row[1]}")
        print(f"Gender            : {row[2]}")
        print(f"Item Purchased    : {row[3]}")
        print(f"Category          : {row[4]}")
        print(f"Purchase Amount   : ${row[5]}")
        print(f"Location          : {row[6]}")
        print(f"Size              : {row[7]}")
        print(f"Color             : {row[8]}")
        print(f"Season            : {row[9]}")
        print(f"Review Rating     : {row[10]}")
        print(f"Subscription      : {row[11]}")
        print(f"Shipping Type     : {row[12]}")
        print(f"Discount Applied  : {row[13]}")
        print(f"Promo Code Used   : {row[14]}")
        print(f"Previous Purchases: {row[15]}")
        print(f"Payment Method    : {row[16]}")
        print(f"Purchase Frequency: {row[17]}")
    else:
        print(f"Customer ID {customer_id} not found.")

    cursor.close()
    conn.close()


# ──────────────────────────────────────────────────────────
#  3. REVENUE BY CATEGORY
# ──────────────────────────────────────────────────────────

def revenue_by_category():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category,
               COUNT(*) AS total_transactions,
               ROUND(SUM(purchase_amount), 2) AS total_revenue,
               ROUND(AVG(purchase_amount), 2) AS avg_order_value
        FROM shopping_behavior
        GROUP BY category
        ORDER BY total_revenue DESC
    """)
    rows = cursor.fetchall()

    print("\n--- REVENUE BY CATEGORY ---")
    print(f"{'Category':<15} {'Transactions':<15} {'Total Revenue':<18} {'Avg Order Value'}")
    print("-" * 65)
    for row in rows:
        print(f"{row[0]:<15} {row[1]:<15} ${row[2]:<17} ${row[3]}")

    cursor.close()
    conn.close()


# ──────────────────────────────────────────────────────────
#  4. TOP 10 BEST SELLING ITEMS
# ──────────────────────────────────────────────────────────

def top_selling_items():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT item_purchased, category,
               COUNT(*) AS purchase_count,
               ROUND(SUM(purchase_amount), 2) AS total_revenue
        FROM shopping_behavior
        GROUP BY item_purchased, category
        ORDER BY purchase_count DESC
        LIMIT 10
    """)
    rows = cursor.fetchall()

    print("\n--- TOP 10 BEST SELLING ITEMS ---")
    print(f"{'#':<4} {'Item':<20} {'Category':<15} {'Count':<10} {'Revenue'}")
    print("-" * 65)
    for i, row in enumerate(rows, 1):
        print(f"{i:<4} {row[0]:<20} {row[1]:<15} {row[2]:<10} ${row[3]}")

    cursor.close()
    conn.close()


# ──────────────────────────────────────────────────────────
#  5. REVENUE BY SEASON
# ──────────────────────────────────────────────────────────

def revenue_by_season():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT season,
               COUNT(*) AS transactions,
               ROUND(SUM(purchase_amount), 2) AS total_revenue,
               ROUND(AVG(review_rating), 2) AS avg_rating
        FROM shopping_behavior
        GROUP BY season
        ORDER BY total_revenue DESC
    """)
    rows = cursor.fetchall()

    print("\n--- REVENUE BY SEASON ---")
    print(f"{'Season':<12} {'Transactions':<15} {'Total Revenue':<18} {'Avg Rating'}")
    print("-" * 60)
    for row in rows:
        print(f"{row[0]:<12} {row[1]:<15} ${row[2]:<17} {row[3]}")

    cursor.close()
    conn.close()


# ──────────────────────────────────────────────────────────
#  6. SUBSCRIBER VS NON-SUBSCRIBER
# ──────────────────────────────────────────────────────────

def subscriber_analysis():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT subscription,
               COUNT(*) AS customers,
               ROUND(AVG(purchase_amount), 2) AS avg_spend,
               ROUND(SUM(purchase_amount), 2) AS total_spend,
               ROUND(AVG(previous_purchases), 1) AS avg_prev_purchases
        FROM shopping_behavior
        GROUP BY subscription
    """)
    rows = cursor.fetchall()

    print("\n--- SUBSCRIBER vs NON-SUBSCRIBER ANALYSIS ---")
    print(f"{'Subscribed':<12} {'Customers':<12} {'Avg Spend':<12} {'Total Spend':<18} {'Avg Prev Purchases'}")
    print("-" * 70)
    for row in rows:
        print(f"{row[0]:<12} {row[1]:<12} ${row[2]:<11} ${row[3]:<17} {row[4]}")

    cursor.close()
    conn.close()


# ──────────────────────────────────────────────────────────
#  7. DISCOUNT AND PROMO CODE IMPACT
# ──────────────────────────────────────────────────────────

def discount_promo_analysis():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT discount_applied, promo_code_used,
               COUNT(*) AS transactions,
               ROUND(AVG(purchase_amount), 2) AS avg_spend
        FROM shopping_behavior
        GROUP BY discount_applied, promo_code_used
        ORDER BY avg_spend DESC
    """)
    rows = cursor.fetchall()

    print("\n--- DISCOUNT AND PROMO CODE IMPACT ---")
    print(f"{'Discount':<12} {'Promo Used':<14} {'Transactions':<15} {'Avg Spend'}")
    print("-" * 55)
    for row in rows:
        print(f"{row[0]:<12} {row[1]:<14} {row[2]:<15} ${row[3]}")

    cursor.close()
    conn.close()


# ──────────────────────────────────────────────────────────
#  8. GENDER CATEGORY PREFERENCE
# ──────────────────────────────────────────────────────────

def gender_category_analysis():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT gender, category,
               COUNT(*) AS purchase_count,
               ROUND(AVG(purchase_amount), 2) AS avg_spend
        FROM shopping_behavior
        GROUP BY gender, category
        ORDER BY gender, purchase_count DESC
    """)
    rows = cursor.fetchall()

    print("\n--- GENDER-WISE CATEGORY PREFERENCE ---")
    print(f"{'Gender':<10} {'Category':<15} {'Purchase Count':<18} {'Avg Spend'}")
    print("-" * 55)
    for row in rows:
        print(f"{row[0]:<10} {row[1]:<15} {row[2]:<18} ${row[3]}")

    cursor.close()
    conn.close()


# ──────────────────────────────────────────────────────────
#  9. PAYMENT METHOD ANALYSIS
# ──────────────────────────────────────────────────────────

def payment_method_analysis():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT payment_method,
               COUNT(*) AS usage_count,
               ROUND(AVG(purchase_amount), 2) AS avg_spend
        FROM shopping_behavior
        GROUP BY payment_method
        ORDER BY usage_count DESC
    """)
    rows = cursor.fetchall()

    print("\n--- PAYMENT METHOD ANALYSIS ---")
    print(f"{'Payment Method':<20} {'Usage Count':<15} {'Avg Spend'}")
    print("-" * 50)
    for row in rows:
        print(f"{row[0]:<20} {row[1]:<15} ${row[2]}")

    cursor.close()
    conn.close()


# ──────────────────────────────────────────────────────────
#  10. AGE GROUP ANALYSIS
# ──────────────────────────────────────────────────────────

def age_group_analysis():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            CASE
                WHEN age BETWEEN 18 AND 25 THEN '18-25 (Gen Z)'
                WHEN age BETWEEN 26 AND 35 THEN '26-35 (Millennials)'
                WHEN age BETWEEN 36 AND 50 THEN '36-50 (Gen X)'
                ELSE '51-70 (Boomers)'
            END AS age_group,
            COUNT(*) AS customers,
            ROUND(AVG(purchase_amount), 2) AS avg_spend,
            ROUND(SUM(purchase_amount), 2) AS total_spend,
            ROUND(AVG(review_rating), 2) AS avg_rating
        FROM shopping_behavior
        GROUP BY age_group
        ORDER BY avg_spend DESC
    """)
    rows = cursor.fetchall()

    print("\n--- AGE GROUP ANALYSIS ---")
    print(f"{'Age Group':<22} {'Customers':<12} {'Avg Spend':<12} {'Total Spend':<18} {'Avg Rating'}")
    print("-" * 72)
    for row in rows:
        print(f"{row[0]:<22} {row[1]:<12} ${row[2]:<11} ${row[3]:<17} {row[4]}")

    cursor.close()
    conn.close()


# ──────────────────────────────────────────────────────────
#  11. TOP 15 STATES BY REVENUE
# ──────────────────────────────────────────────────────────

def top_locations():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT location,
               COUNT(*) AS transactions,
               ROUND(SUM(purchase_amount), 2) AS total_revenue,
               ROUND(AVG(purchase_amount), 2) AS avg_spend
        FROM shopping_behavior
        GROUP BY location
        ORDER BY total_revenue DESC
        LIMIT 15
    """)
    rows = cursor.fetchall()

    print("\n--- TOP 15 STATES BY REVENUE ---")
    print(f"{'#':<4} {'State':<22} {'Transactions':<15} {'Total Revenue':<18} {'Avg Spend'}")
    print("-" * 68)
    for i, row in enumerate(rows, 1):
        print(f"{i:<4} {row[0]:<22} {row[1]:<15} ${row[2]:<17} ${row[3]}")

    cursor.close()
    conn.close()


# ──────────────────────────────────────────────────────────
#  12. PURCHASE FREQUENCY ANALYSIS
# ──────────────────────────────────────────────────────────

def frequency_analysis():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT purchase_frequency,
               COUNT(*) AS customers,
               ROUND(SUM(purchase_amount), 2) AS total_revenue,
               ROUND(AVG(purchase_amount), 2) AS avg_spend
        FROM shopping_behavior
        GROUP BY purchase_frequency
        ORDER BY total_revenue DESC
    """)
    rows = cursor.fetchall()

    print("\n--- PURCHASE FREQUENCY ANALYSIS ---")
    print(f"{'Frequency':<20} {'Customers':<12} {'Total Revenue':<18} {'Avg Spend'}")
    print("-" * 62)
    for row in rows:
        print(f"{row[0]:<20} {row[1]:<12} ${row[2]:<17} ${row[3]}")

    cursor.close()
    conn.close()


# ──────────────────────────────────────────────────────────
#  13. SHIPPING TYPE ANALYSIS
# ──────────────────────────────────────────────────────────

def shipping_analysis():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT shipping_type,
               COUNT(*) AS usage_count,
               ROUND(AVG(purchase_amount), 2) AS avg_spend,
               ROUND(SUM(purchase_amount), 2) AS total_revenue
        FROM shopping_behavior
        GROUP BY shipping_type
        ORDER BY usage_count DESC
    """)
    rows = cursor.fetchall()

    print("\n--- SHIPPING TYPE ANALYSIS ---")
    print(f"{'Shipping Type':<20} {'Usage Count':<15} {'Avg Spend':<15} {'Total Revenue'}")
    print("-" * 65)
    for row in rows:
        print(f"{row[0]:<20} {row[1]:<15} ${row[2]:<14} ${row[3]}")

    cursor.close()
    conn.close()


# ──────────────────────────────────────────────────────────
#  14. ADD NEW CUSTOMER RECORD
# ──────────────────────────────────────────────────────────

def add_customer():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT MAX(customer_id) FROM shopping_behavior")
    max_id = cursor.fetchone()[0]
    new_id = (max_id or 0) + 1
    print(f"New Customer ID will be: {new_id}")

    age               = int(input("Enter Age: "))
    gender            = input("Enter Gender (Male/Female): ")
    item_purchased    = input("Enter Item Purchased: ")
    category          = input("Enter Category (Clothing/Footwear/Accessories/Outerwear): ")
    purchase_amount   = float(input("Enter Purchase Amount (USD): "))
    location          = input("Enter Location (State): ")
    size              = input("Enter Size (S/M/L/XL): ")
    color             = input("Enter Color: ")
    season            = input("Enter Season (Spring/Summer/Fall/Winter): ")
    review_rating     = float(input("Enter Review Rating (1.0 to 5.0): "))
    subscription      = input("Subscription Status (Yes/No): ")
    shipping_type     = input("Enter Shipping Type (Express/Standard/Free Shipping etc): ")
    discount_applied  = input("Discount Applied (Yes/No): ")
    promo_code_used   = input("Promo Code Used (Yes/No): ")
    previous_purchases= int(input("Previous Purchases count: "))
    payment_method    = input("Payment Method (Credit Card/PayPal/Cash etc): ")
    purchase_frequency= input("Purchase Frequency (Weekly/Monthly/Annually etc): ")

    cursor.execute("""
        INSERT INTO shopping_behavior VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        new_id, age, gender, item_purchased, category, purchase_amount,
        location, size, color, season, review_rating, subscription,
        shipping_type, discount_applied, promo_code_used,
        previous_purchases, payment_method, purchase_frequency
    ))

    conn.commit()
    print(f"\nCustomer {new_id} added successfully!")
    cursor.close()
    conn.close()


# ──────────────────────────────────────────────────────────
#  15. DELETE CUSTOMER RECORD
# ──────────────────────────────────────────────────────────

def delete_customer():
    customer_id = input("Enter Customer ID to delete: ").strip()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT customer_id, gender, item_purchased, purchase_amount FROM shopping_behavior WHERE customer_id = %s", (customer_id,))
    row = cursor.fetchone()

    if not row:
        print(f"Customer ID {customer_id} not found.")
        cursor.close()
        conn.close()
        return

    print(f"\nFound: ID={row[0]}, Gender={row[1]}, Item={row[2]}, Amount=${row[3]}")
    confirm = input("Are you sure you want to delete? (yes/no): ")

    if confirm.lower() == "yes":
        cursor.execute("DELETE FROM shopping_behavior WHERE customer_id = %s", (customer_id,))
        conn.commit()
        print("Customer record deleted successfully.")
    else:
        print("Delete cancelled.")

    cursor.close()
    conn.close()


# ──────────────────────────────────────────────────────────
#  16. OVERALL SUMMARY STATS
# ──────────────────────────────────────────────────────────

def overall_summary():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM shopping_behavior")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT ROUND(SUM(purchase_amount),2) FROM shopping_behavior")
    total_rev = cursor.fetchone()[0]

    cursor.execute("SELECT ROUND(AVG(purchase_amount),2) FROM shopping_behavior")
    avg_spend = cursor.fetchone()[0]

    cursor.execute("SELECT ROUND(AVG(review_rating),2) FROM shopping_behavior")
    avg_rating = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM shopping_behavior WHERE subscription='Yes'")
    subscribers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM shopping_behavior WHERE discount_applied='Yes'")
    discounted = cursor.fetchone()[0]

    cursor.execute("SELECT category, COUNT(*) as cnt FROM shopping_behavior GROUP BY category ORDER BY cnt DESC LIMIT 1")
    top_cat = cursor.fetchone()

    cursor.execute("SELECT item_purchased, COUNT(*) as cnt FROM shopping_behavior GROUP BY item_purchased ORDER BY cnt DESC LIMIT 1")
    top_item = cursor.fetchone()

    cursor.execute("SELECT payment_method, COUNT(*) as cnt FROM shopping_behavior GROUP BY payment_method ORDER BY cnt DESC LIMIT 1")
    top_pay = cursor.fetchone()

    print("\n======== OVERALL SUMMARY ========")
    print(f"Total Records          : {total}")
    print(f"Total Revenue          : ${total_rev}")
    print(f"Average Order Value    : ${avg_spend}")
    print(f"Average Review Rating  : {avg_rating} / 5.0")
    print(f"Total Subscribers      : {subscribers}")
    print(f"Discount Used Count    : {discounted}")
    print(f"Top Category           : {top_cat[0]} ({top_cat[1]} sales)")
    print(f"Top Selling Item       : {top_item[0]} ({top_item[1]} sales)")
    print(f"Most Used Payment      : {top_pay[0]} ({top_pay[1]} times)")

    cursor.close()
    conn.close()


# ──────────────────────────────────────────────────────────
#  EXPORT REPORT TO TXT FILE
# ──────────────────────────────────────────────────────────

def export_report():
    conn = get_connection()
    cursor = conn.cursor()

    report = []
    report.append("=" * 55)
    report.append("   CUSTOMER TREND ANALYSIS - SUMMARY REPORT")
    report.append("=" * 55)

    # Overall stats
    cursor.execute("SELECT COUNT(*), ROUND(SUM(purchase_amount),2), ROUND(AVG(purchase_amount),2), ROUND(AVG(review_rating),2) FROM shopping_behavior")
    row = cursor.fetchone()
    report.append(f"\n[OVERVIEW]")
    report.append(f"Total Records    : {row[0]}")
    report.append(f"Total Revenue    : ${row[1]}")
    report.append(f"Avg Order Value  : ${row[2]}")
    report.append(f"Avg Rating       : {row[3]}")

    # Revenue by category
    cursor.execute("SELECT category, ROUND(SUM(purchase_amount),2) FROM shopping_behavior GROUP BY category ORDER BY 2 DESC")
    report.append(f"\n[REVENUE BY CATEGORY]")
    for r in cursor.fetchall():
        report.append(f"  {r[0]:<20} ${r[1]}")

    # Revenue by season
    cursor.execute("SELECT season, ROUND(SUM(purchase_amount),2) FROM shopping_behavior GROUP BY season ORDER BY 2 DESC")
    report.append(f"\n[REVENUE BY SEASON]")
    for r in cursor.fetchall():
        report.append(f"  {r[0]:<20} ${r[1]}")

    # Top 10 items
    cursor.execute("SELECT item_purchased, COUNT(*), ROUND(SUM(purchase_amount),2) FROM shopping_behavior GROUP BY item_purchased ORDER BY 2 DESC LIMIT 10")
    report.append(f"\n[TOP 10 ITEMS BY SALES]")
    for i, r in enumerate(cursor.fetchall(), 1):
        report.append(f"  {i}. {r[0]:<20} {r[1]} sales   ${r[2]}")

    # Payment methods
    cursor.execute("SELECT payment_method, COUNT(*) FROM shopping_behavior GROUP BY payment_method ORDER BY 2 DESC")
    report.append(f"\n[PAYMENT METHOD USAGE]")
    for r in cursor.fetchall():
        report.append(f"  {r[0]:<20} {r[1]} transactions")

    # Top 10 states
    cursor.execute("SELECT location, ROUND(SUM(purchase_amount),2) FROM shopping_behavior GROUP BY location ORDER BY 2 DESC LIMIT 10")
    report.append(f"\n[TOP 10 STATES BY REVENUE]")
    for i, r in enumerate(cursor.fetchall(), 1):
        report.append(f"  {i}. {r[0]:<22} ${r[1]}")

    report.append("\n" + "=" * 55)
    report.append("   END OF REPORT")
    report.append("=" * 55)

    filename = "customer_trend_report.txt"
    with open(filename, "w") as f:
        f.write("\n".join(report))

    print(f"\nReport exported successfully as: {filename}")
    cursor.close()
    conn.close()


# ──────────────────────────────────────────────────────────
#  MAIN MENU
# ──────────────────────────────────────────────────────────

def main_menu():
    while True:
        print("\n======== CUSTOMER TREND ANALYSIS SYSTEM ========")
        print("1.  Setup Database, Table & Insert Sample Data")
        print("2.  View All Customers (first 20)")
        print("3.  Search Customer by ID")
        print("4.  Revenue by Category")
        print("5.  Top 10 Best Selling Items")
        print("6.  Revenue by Season")
        print("7.  Subscriber vs Non-Subscriber Analysis")
        print("8.  Discount & Promo Code Impact")
        print("9.  Gender Category Preference")
        print("10. Payment Method Analysis")
        print("11. Age Group Analysis")
        print("12. Top 15 States by Revenue")
        print("13. Purchase Frequency Analysis")
        print("14. Shipping Type Analysis")
        print("15. Add New Customer Record")
        print("16. Delete Customer Record")
        print("17. Overall Summary Stats")
        print("18. Export Report to TXT File")
        print("0.  Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            setup_database()
        elif choice == "2":
            view_all_customers()
        elif choice == "3":
            search_customer()
        elif choice == "4":
            revenue_by_category()
        elif choice == "5":
            top_selling_items()
        elif choice == "6":
            revenue_by_season()
        elif choice == "7":
            subscriber_analysis()
        elif choice == "8":
            discount_promo_analysis()
        elif choice == "9":
            gender_category_analysis()
        elif choice == "10":
            payment_method_analysis()
        elif choice == "11":
            age_group_analysis()
        elif choice == "12":
            top_locations()
        elif choice == "13":
            frequency_analysis()
        elif choice == "14":
            shipping_analysis()
        elif choice == "15":
            add_customer()
        elif choice == "16":
            delete_customer()
        elif choice == "17":
            overall_summary()
        elif choice == "18":
            export_report()
        elif choice == "0":
            print("Exiting... Bye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()