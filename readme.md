# Scalable Banking API -  Transaction Processing and Consistency

Video Walkthrough: https://www.loom.com/share/fdc0e8186c0241e9989d2bc4431b2bdf

1. To Design a Restful API for processing transactions with the following requirements:

<ul>
<li>
Supports Credit, Debit and Balance Enquiry Operations: To support the three operations, we have to have an Account Table in the database, where we will first store the balance information, which can be added to in case of a credit operation and subtracted from in case of a debit operation. The same balance can be queries in case of a balance enquiry operation. This logic can be then securely exposed over an API to allow an authorised user to perform the operations.
</li>
<li>
Ensures Atomicity - A Transction can not be partially completed: So, when a transaction, suppose debit is initiated, technically and logically, what happens is that the specified amount is subtracted from the user's account, if the available balance allows it, and the same amount is added to the beneficiary's account. So, there are two database writes involved, where one is to debited user account and the other is to credit beneficiary account. One more write is added, which is to store the Transaction data anywhere. If anything goes wrong, after one DB write, that would be a major transactional issue. The solution to this is atomicity, which means a transaction, which includes multiple steps has to completed from start to end, without fail. If all steps are completed, then only the changes are <strong>committed</strong>. If any of the step goes wrong in the middle, all the steps, even the passed ones are <strong> rolled back </strong>. 
</li>
<li>
Handles concurrent requests efficiently: Concurrency is a must in platforms handling large traffic volumes. If multiple users try to write to the same row of the database simoultanesouly, they would run into a <strong> Race Condition </strong>. To handle this successfully, we need to implement row locking. So, that as soon as a user tries to carry out a transaction, the database row would be locked till the transaction is complete, in order to make sure that no other user does an update to the same row in the meantime.
</li>
<li>
Returns clear error messages in failure cases: So, if a failure happens, a clear error message should be returned as the response
</li>
</ul>

2. Explain
<ul>
<li>
 Database Schema: Since the data to be stored would be structured, so I would prefer using a SQL based database, preferrably PostgreSQL.  The schema would be as follows

<ul>

1. Account Table

| Column  | Data Type    | Constraints                      |
|---------|--------------|----------------------------------|
| `account_id`    | Integer      | Primary Key, Auto-increment      |
| `holder_name`  | String(100)  | Not Null                         |
| `available_balance` | Float      | Not Null, Default = `0.0`        |

This table shall be used to store all the Accounts, along with the necessary information.

2. Transaction Table

| Column  | Data Type    | Constraints                      |
|---------|--------------|----------------------------------|
| `transaction_id`    | Integer      | Primary Key, Auto-increment      |
| `account_id`    | Integer      | FK to account table (account_id), Not Null      |
| `amount`  | Float  | Not Null                         |
| `transaction_type` | String(10)      | `Credit` or `Debit`        |
| `transaction_status` | String(10)      | `Success` or `Failure`        |
| `timestamp` | DateTime     |  -       |

This table shall be used to store all the Transactions that have been carried out
</ul>
</li>
<li>
In order to ensure consitency in case of a crash mid-transaction, I'd use the concept of <strong>Context Managers</strong> provided by SQLAlchemy, which is an ORM that I'll be using for my database interactions. Context managers wrap all database operations in a transaction, which if completed succesfully, is committed to the database, else is rolled back, so that the database doesn't store any inconsistent or partial changes. Context Managers can be used with PostrgeSQL as well as Postgres is ACID compliant.
</li>
<li>
High perfomance can be ensureed by making optimizations at different levels of the application.

1. At the Application Level, we can implement Caching of the frequently accessed data using Redis, but it has to be very well managed, so that cache data is invalidated as soon as the actual data changes in the DB.
2. At the database level, we can implement Database indexing strategically in a way on the fields that are queried the most. For e.g if we use account_id to query the specific account, we can index this very field to ensure a faster lookup. Also, using efficient queries by retrieving only the required data optimizes the performance.
</li>
</ul>

## Building the API

In order to build the API, I will use the following tech stack

<ul>
<li>Flask for Backend</li>
<li>Postgres for Database</li>
<li>SQL Alchemy as ORM</li>
<li>Render for Deployment</li>
<li> Docker for containerizing and quick + secure BE and DB setup </li>
</ul>