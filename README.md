# Customer Trend Analysis System

A comprehensive Python-based application for analyzing customer shopping behavior patterns using MySQL database. This system provides detailed insights into customer trends, revenue analysis, and behavioral patterns through an interactive command-line interface.

## Features

- **Database Management**: Automated setup of MySQL database and tables with sample data
- **Customer Analysis**: View, search, add, and delete customer records
- **Revenue Analytics**: 
  - Revenue breakdown by category, season, and location
  - Top-selling items and payment method analysis
- **Demographic Insights**: Age group analysis, gender preferences, and subscriber behavior
- **Marketing Analysis**: Discount and promo code impact assessment
- **Reporting**: Export comprehensive analysis reports to text files
- **Interactive Menu**: User-friendly command-line interface for all operations

## Prerequisites

- Python 3.6 or higher
- MySQL Server 5.7 or higher
- MySQL Connector/Python library

## Installation

1. **Clone or Download** the project files to your local machine.

2. **Install Dependencies**:
   ```bash
   pip install mysql-connector-python
   ```

3. **Database Setup**:
   - Ensure MySQL Server is installed and running on your system
   - Update the database connection credentials in `main.py` if necessary:
     ```python
     host="localhost",
     user="root",
     password="your_mysql_password",  # Change this to your MySQL password
     database="customer_trends"
     ```

## Usage

1. **Run the Application**:
   ```bash
   python main.py
   ```

2. **Initial Setup**:
   - Choose option `1` from the main menu to create the database, tables, and insert sample data

3. **Navigate the Menu**:
   - Use the numbered options (1-18) to perform various analyses
   - Option `0` to exit the application

## Database Schema

The system uses a single table `shopping_behavior` with the following structure:

- `customer_id` (INT, PRIMARY KEY)
- `age` (INT)
- `gender` (VARCHAR)
- `item_purchased` (VARCHAR)
- `category` (VARCHAR)
- `purchase_amount` (DECIMAL)
- `location` (VARCHAR)
- `size` (VARCHAR)
- `color` (VARCHAR)
- `season` (VARCHAR)
- `review_rating` (DECIMAL)
- `subscription` (VARCHAR)
- `shipping_type` (VARCHAR)
- `discount_applied` (VARCHAR)
- `promo_code_used` (VARCHAR)
- `previous_purchases` (INT)
- `payment_method` (VARCHAR)
- `purchase_frequency` (VARCHAR)

## Menu Options

1. **Setup Database**: Initialize database, create tables, and insert sample data
2. **View All Customers**: Display first 20 customer records
3. **Search Customer**: Find customer by ID with full details
4. **Revenue by Category**: Analyze sales performance across product categories
5. **Top Selling Items**: Identify best-performing products
6. **Revenue by Season**: Seasonal sales analysis
7. **Subscriber Analysis**: Compare subscriber vs non-subscriber behavior
8. **Discount Impact**: Evaluate discount and promo code effectiveness
9. **Gender Preferences**: Analyze shopping patterns by gender
10. **Payment Methods**: Payment method usage statistics
11. **Age Group Analysis**: Demographic spending patterns
12. **Top Locations**: Revenue analysis by state/location
13. **Purchase Frequency**: Analyze buying frequency patterns
14. **Shipping Analysis**: Shipping type preferences and impact
15. **Add Customer**: Insert new customer records
16. **Delete Customer**: Remove customer records
17. **Summary Statistics**: Overall business metrics
18. **Export Report**: Generate comprehensive analysis report

## Data Source

The project includes sample data for demonstration. For production use, you can:
- Modify the sample data insertion in the `setup_database()` function
- Import data from the provided `customer_shopping_behavior.csv` file (requires additional CSV import functionality)

## Troubleshooting

- **Connection Issues**: Ensure MySQL server is running and credentials are correct
- **Import Errors**: Verify that `mysql-connector-python` is installed
- **Permission Errors**: Ensure your MySQL user has database creation privileges

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open-source and available under the MIT License.

## Support

For questions or issues, please check the troubleshooting section or create an issue in the repository.
