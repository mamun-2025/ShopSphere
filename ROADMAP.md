

# 🚀 ShopSphere --- Development Roadmap
- Project: ShopSphere --- Django E-commerce Backend
- Purpose: Build a practical, production-oriented e-commerce backend
while developing strong backend engineering, database, API, testing,
and deployment skills.
- Roadmap status: M1--M6 completed; M7 in progress; M8 onward
planned/in progress as described below.

---

# 🎯 1. Project Overview
ShopSphere is a Django-based e-commerce application. The project is
being developed incrementally, starting with core e-commerce
functionality and progressing toward a robust backend architecture with
APIs, authentication, testing, delivery management, background
processing, real-time updates, and production deployment.

The roadmap separates implemented functionality from future
engineering goals. A feature should be marked complete only after
implementation and testing.
Learning and development workflow
For each major topic, follow this cycle:
1. Learn the concept and terminology.
2. Understand why it is needed and how it works.
3. Implement it in a small, controlled example.
4. Integrate it into ShopSphere where appropriate.
5. Experiment with edge cases and failure scenarios.
6. Test expected and unexpected behavior.
7. Document the implementation and decisions.
8. Commit stable changes to Git.

---

# 🛠️ 2. Technology Stack

```text
   Category                      Technology
   ____________________          _______________________________________
1. Programming Language          ➡️ Python
2. Backend Framework             ➡️ Django
3. Database ORM                  ➡️ Django ORM
4. Database                      ➡️ PostgreSQL
5. API Development               ➡️ Django REST Framework (DRF)
6. Authentication                ➡️ Custom User Model, RBAC, JWT
7. Payment Gateway               ➡️ SSLCommerz Sandbox
8. Frontend                      ➡️ HTML, CSS, JavaScript, Bootstrap
9. File Handling                 ➡️ Pillow, Django FileField, ImageField
10. Background Tasks             ➡️ Celery
11. Message Broker/Cache         ➡️ Redis
12. Real-Time Communication      ➡️ Django Channels, WebSocket, ASGI
13. GPS & Location               ➡️ Browser Geolocation API
14. Map Integration              ➡️ Map API
15. Web Server                   ➡️ Gunicorn, Uvicorn, Nginx
16. Containerization             ➡️ Docker, Docker Compose
17. Operating System             ➡️ Linux
18. Version Control              ➡️ Git, GitHub

```
---

# 📌 3. Project Status

| Milestone    | Status |
| ------------ | ------ |
| Milestone 1  | ✅ Completed|
| Milestone 2  | ✅ Completed|
| Milestone 3  | ✅ Completed|
| Milestone 4  | ✅ Completed|
| Milestone 5  | ✅ Completed|
| Milestone 6  | ✅ Completed|
| Milestone 7  | 🟨 In Progress|
| Milestone 8  | ⬜ Not Started|
| Milestone 9  | ⬜ Not Started|
| Milestone 10 | ⬜ Not Started|
| Milestone 11 | ⬜ Not Started|
| Milestone 12 | ⬜ Not Started|
| Milestone 13 | ⬜ Not Started|
| Milestone 14 | ⬜ Not Started|

Legend:

* ⬜ Not Started
* 🟨 In Progress
* ✅ Completed

---

# 🛣️ 4. Detailed Development Roadmap

## 🟢 Milestone 01 — Project Foundation & Authentication

**Status:** ✅ Completed

### Topics

* [✅] Project Setup
* [✅] Custom User Model
* [✅] Register
* [✅] Login
* [✅] Logout
* [✅] User Profile
* [✅] Edit Profile
* [✅] Password Change
* [✅] Password Reset
* [✅] Bootstrap Layout

### Output

* [✅] Professional Authentication System

---

## 🟢 Milestone 2 — Milestone 02 — Categories & Product Management (CBV)

**Status:** ✅ Completed

### Topics

* [✅] Class-Based Views (CBV)
* [✅] ListView
* [✅] CreateView
* [✅] UpdateView
* [✅] DeleteView
* [✅] Categorie Model
* [✅] Categorie Management
* [✅] Product Model
* [✅] Product ListView
* [✅] Product DetailView
* [✅] Product CreateView
* [✅] Product UpdateView
* [✅] Product DeleteView
* [✅] Slug Management
* [✅] Product Search
* [✅] Pagination

### Output

* [✅] Professional Category & Product Management System

---

## 🟢 Milestone 3 — File Handling & Media Management

**Status:** ✅ Completed

### Topics

* [✅] MEDIA_ROOT
* [✅] MEDIA_URL
* [✅] Pillow Insatallation
* [✅] ImageField
* [✅] Product Image Upload
* [✅] Multiple Image Upload 
* [✅] FileField
* [✅] PDF Upload
* [✅] PDF Extension Validation
* [✅] File Size Validator
* [✅] Main Image Deletion
* [✅] Main Image Replacement
* [✅] PDF Image Deletion
* [✅] PDF Image Replacement
* [✅] Gallery Image Deletion
* [✅] Gallery Image Replacement
* [✅] Product Delete → All Gallery Files Cleanup

### Output

* [✅] Complete Product File & Media Management System

---

## 🟢 Milestone 4 — Product Reviews & Moderation

**Status:** ✅ Completed

### Topics

* [✅] Review App Setup
* [✅] Review Model
* [✅] Rating System
* [✅] Review Form
* [✅] Create Review
* [✅] Duplicate Review Protection
* [✅] Display Reviews
* [✅] Average Rating Calculation
* [✅] Rating Distribution
* [✅] Dynamic Star Ratings
* [✅] Database Annotation
* [✅] Update Review
* [✅] Delete Review
* [✅] Review Moderation


### Output

* [✅] Product Review & Rating System

---

## 🟢 Milestone 5 — Authorization [Role-Based Access Control (RBAC)]

**Status:** ✅ Completed

### Topics

* [✅] Django Permissions
* [✅] Django Groups
* [✅] Role Management
* [✅] Customer Authorization
* [✅] Staff Authorization 
* [✅] Manager Authorization 
* [✅] Admin Authorization 
* [✅] Object-Level Authorization
* [✅] CBV Authorization
* [✅] Function-Based Authorization
* [✅] Template Authorization  
* [✅] Django Admin Security   
* [✅] Full Authorization Testing    


### Output

* [✅] Role-Based Access Control (RBAC)
* [✅] Permission-Based Authorization
* [✅] Object-Level Authorization
* [✅] CBV/FBV Authorization
* [✅] Permission-Aware User Interface
* [✅] Authorization Test Coverage

---

## 🟢 Milestone 6 — Inventory Management

**Status:** ✅ Completed

### Topics 

* [✅] Inventory Model
* [✅] SKU Management
* [✅] Low Stock Management
* [✅] Out of Stock Management
* [✅] Stock Increase
* [✅] Stock Decrease
* [✅] Stock Validation
* [✅] Inventory Admin
* [✅] Inventory Views
* [✅] Inventory User Interface


### Output

* [✅] Inventory Management System

---

## 🟢 Milestone 7 — Business Logic

**Status:** 🟨 In Progress

### Topics

1. Shopping Cart & Wishlist

* [✅] Shopping Cart
* [✅] Add to Cart
* [✅] Update Cart Quantity
* [✅] Remove Cart Item
* [✅] Wishlist
* [✅] Add to Wishlist
* [✅] Remove from Wishlist

2. Tax & Shipping Management

* [✅] Tax Management
* [✅] Tax Calculation
* [✅] Shipping Management
* [✅] Shipping Zones
* [✅] Shipping Methods
* [✅] Shipping Fee Calculation
* [✅] Shipping Address Management

3. Checkout & Order Processing

* [✅] Checkout System
* [✅] Buy Now Functionality
* [✅] Cart Checkout
* [✅] Core Order Management
* [✅] Order Creation
* [✅] Order History
* [✅] Order Details
* [✅] Customer Order Cancellation Testing
* [✅] Order Status Transition Validation

4. Payment System

* [✅] Payment App Setup
* [✅] Payment Model
* [✅] Payment Methods
* [✅] Payment Status Management
* [✅] Multiple Payment Attempts
* [✅] Payment Processing — Payment Service ও Lifecycle
* [✅] SSLCommerz Sandbox Integration
* [✅] Server-Side Payment Verification
* [✅] Payment Callback / IPN
* [✅] Duplicate Payment Prevention (Idempotency)
* [✅] Payment Failure Handling
* [ ] Refund Management Foundation

5. Admin Order Management

* [✅] Order Management Dashboard
* [✅] Admin Order Status Management
* [✅] Order Status Transition Rules
* [✅] Order Processing Workflow
* [✅] Order Cancellation Management
* [✅] Stock Restoration on Cancellation

6. Coupon & Discount Management

* [✅] Coupon Model
* [✅] Percentage Discount
* [✅] Fixed Amount Discount
* [✅] Coupon Validation
* [✅] Expiration Date
* [✅] Minimum Order Amount
* [✅] Coupon Usage Limits
* [✅] Discount Calculation

7. Invoice Generation

* [✅] Invoice Model / Numbering
* [✅] PDF Invoice Generation
* [✅] Invoice Download
* [✅] Invoice Access Control

## Output

* [✅] Complete E-commerce Business Logic
* [✅] Payment Processing System
* [✅] Complete Order Management System
* [✅] PDF Invoice Generation


---

## 🟢 Milestone 8 — Signals & Database Transactions

**Status:** ⬜ Not Started

### Topics

1. Django Signals Fundamentals
- [✅] What Are Django Signals?
- [✅] Why Signals Are Used
- [✅] Signal, Sender, Receiver, Dispatcher
- [✅] Signal Lifecycle
- [✅] Synchronous Signal Execution
- [✅] Built-in Django Signals
- [✅] Signal Use Cases and Limitations
2. Model Signals
- [✅] pre_save
- [✅] post_save
- [✅] pre_delete
- [✅] post_delete
- [✅] m2m_changed (Advanced / When Needed)
- [✅] Signal Receiver Arguments
- [✅] created, raw, using, update_fields
- [✅] QuerySet update() and Bulk Operation Limitations
3. Signal Registration & Best Practices
- [✅] signals.py
- [✅] AppConfig
- [✅] AppConfig.ready()
- [✅] @receiver
- [✅] Explicit Signal Registration
- [✅] dispatch_uid
- [✅] Avoiding Duplicate Registration
- [✅] Avoiding Recursive save() Calls
- [✅] Keeping Receivers Small
- [✅] Signal Testing
4. Database Transaction Fundamentals
- [ ] What Is a Database Transaction?
- [ ] Why Transactions Are Needed
- [ ] ACID Properties
- [ ] Atomicity
- [ ] Consistency
- [ ] Isolation
- [ ] Durability
- [ ] Commit
- [ ] Rollback
- [ ] Transaction Boundaries
5. Django Transaction Management
- [ ] transaction.atomic()
- [ ] Atomic Blocks
- [ ] Nested Atomic Blocks
- [ ] Savepoints
- [ ] Exception Handling
- [ ] Transaction Rollback
- [ ] ATOMIC_REQUESTS (Concept and Trade-offs)
- [ ] transaction.on_commit()
- [ ] Why post_save Does Not Mean Transaction Commit
6. Database Integrity & Concurrency
- [ ] Database Constraints
- [ ] Unique Constraints
- [ ] Check Constraints
- [ ] Foreign Key Integrity
- [ ] IntegrityError
- [ ] Race Conditions
- [ ] Concurrent Requests
- [ ] select_for_update()
- [ ] Locking Fundamentals
- [ ] Safe Stock Update Patterns
7. Service Layer Architecture
- [ ] What Is a Service Layer?
- [ ] Why Business Logic Should Not Live in Views
- [ ] Service Functions and Modules
- [ ] Model Responsibilities
- [ ] View Responsibilities
- [ ] Signal Responsibilities
- [ ] Transaction Boundaries in Services
- [ ] Error Handling in Services
- [ ] Service Layer Testing
8. Reliable ShopSphere Workflows
- [ ] Review Existing Order Services
- [ ] Review Inventory Services
- [ ] Review Payment Services
- [ ] Identify Appropriate Signal Use Cases
- [ ] Keep Order Cancellation in Services
- [ ] Keep Stock Deduction / Restoration in Services
- [ ] Keep Payment Verification in Services
- [ ] Trigger Post-Commit Work with on_commit()
- [ ] Prepare Background Task Integration
- [ ] Document Workflow Decisions
9. Milestone 08 Testing
- [ ] Signal Receiver Tests
- [ ] Signal Registration Tests
- [ ] Transaction Commit Tests
- [ ] Rollback Tests
- [ ] on_commit() Tests
- [ ] Constraint Tests
- [ ] Stock Concurrency Tests
- [ ] Order Workflow Integration Tests
Output
- [ ] Appropriate Signal Architecture
- [ ] Reliable Database Transactions
- [ ] Transaction-Safe Order Processing
- [ ] Service Layer Architecture
- [ ] Tested Business Workflows
Important architecture rules
- Signals: model event notification and small decoupled reactions.
- Service Layer: core business operations and business rules.
- transaction.atomic(): database consistency across related
  operations.
- transaction.on_commit(): actions that must wait until a
  successful commit.
- Celery: slow or retryable background work.
Inspect the existing ShopSphere code before changing it. Do not add
signals just because a signal exists.

---

## 🟢 Milestone 9 — PostgreSQL Integration

**Status:** ⬜ Not Started

### Topics

1. PostgreSQL Fundamentals
- [ ] PostgreSQL Introduction
- [ ] PostgreSQL vs SQLite
- [ ] PostgreSQL Installation
- [ ] PostgreSQL Service Management
- [ ] Database Creation
- [ ] Database Users and Roles
- [ ] Database Privileges
- [ ] PostgreSQL Shell (psql)
- [ ] Basic SQL Commands
- [ ] Tables, Rows, and Columns
2. Django PostgreSQL Integration
- [ ] Install PostgreSQL Driver (psycopg)
- [ ] Configure Database Credentials
- [ ] Environment Variables
- [ ] Django PostgreSQL Settings
- [ ] Connect Django to PostgreSQL
- [ ] Verify Database Connection
- [ ] SQLite to PostgreSQL Migration
- [ ] Apply Django Migrations
- [ ] Migration Conflicts
- [ ] Migration Rollback
- [ ] Data Migration
- [ ] Verify Migrated Data
3. SQL Fundamentals for Backend Developers
- [ ] SELECT
- [ ] INSERT
- [ ] UPDATE
- [ ] DELETE
- [ ] WHERE
- [ ] ORDER BY
- [ ] GROUP BY
- [ ] Aggregate Functions
- [ ] JOIN Operations
- [ ] Subqueries (Introduction)
- [ ] SQL Constraints
- [ ] SQL Transactions
4. Database Design
- [ ] Primary Keys
- [ ] Foreign Keys
- [ ] Unique Constraints
- [ ] Check Constraints
- [ ] NOT NULL Constraints
- [ ] One-to-One Relationships
- [ ] One-to-Many Relationships
- [ ] Many-to-Many Relationships
- [ ] Database Normalization (Fundamentals)
- [ ] Practical Schema Review
5. Django ORM Query Optimization
- [ ] QuerySet Evaluation
- [ ] Lazy QuerySets
- [ ] select_related()
- [ ] prefetch_related()
- [ ] N+1 Query Problem
- [ ] annotate()
- [ ] aggregate()
- [ ] only() and defer()
- [ ] values() and values_list()
- [ ] Bulk Operations and Their Trade-offs
- [ ] Django Debug Toolbar
- [ ] QuerySet.explain()
6. Indexing & Performance
- [ ] What Is a Database Index?
- [ ] Single-Column Index
- [ ] Composite Index
- [ ] Unique Index
- [ ] Index Trade-offs
- [ ] Query Execution Plans
- [ ] Slow Query Identification
- [ ] Practical Query Optimization
- [ ] Measure Before and After Optimization
7. Database Administration
- [ ] pg_dump
- [ ] pg_restore
- [ ] Plain SQL Backup
- [ ] Custom Format Backup
- [ ] Database Restore
- [ ] Backup Verification
- [ ] Database Monitoring Fundamentals
- [ ] Connection Management
- [ ] Database Maintenance Basics
Output
- [ ] PostgreSQL-Integrated ShopSphere
- [ ] Verified SQLite-to-PostgreSQL Migration
- [ ] Reliable Database Schema
- [ ] Optimized ORM Queries
- [ ] Database Backup and Recovery Procedure

---

## 🟢 Milestone 10 — Django REST Framework (DRF)

**Status:** ⬜ Not Started

### Topics

1. API & HTTP Fundamentals
- [ ] What Is an API?
- [ ] What Is REST?
- [ ] REST Constraints (Overview)
- [ ] HTTP Request and Response
- [ ] HTTP Methods
- [ ] HTTP Status Codes
- [ ] Headers
- [ ] JSON
- [ ] Query Parameters
- [ ] Request Body
- [ ] Idempotent HTTP Methods
- [ ] API Error Response Design
2. DRF Setup
- [ ] Install Django REST Framework
- [ ] Configure DRF
- [ ] API URL Structure
- [ ] API Root
- [ ] Browsable API
- [ ] Default Renderer and Parser Concepts
3. Serializers & Validation
- [ ] Serializer Fundamentals
- [ ] Serializer
- [ ] ModelSerializer
- [ ] Serializer Fields
- [ ] Field-Level Validation
- [ ] Object-Level Validation
- [ ] Custom Validation
- [ ] Read-Only and Write-Only Fields
- [ ] Nested Serializers
- [ ] Serializer Relationships
- [ ] Serializer Error Responses
4. API Views & Routing
- [ ] APIView
- [ ] GenericAPIView
- [ ] Mixins
- [ ] Generic Views
- [ ] ViewSets
- [ ] ModelViewSet
- [ ] Custom Actions
- [ ] Routers
- [ ] Function-Based API Views (Overview)
- [ ] Choosing the Right View Type
5. API Authentication & Permissions
- [ ] DRF Authentication Fundamentals
- [ ] Session Authentication
- [ ] Basic Authentication (Concept and Cautions)
- [ ] Permission Classes
- [ ] Custom Permissions
- [ ] Object-Level Permissions
- [ ] Role-Based API Authorization
- [ ] Ownership Checks
- [ ] Throttling
- [ ] CORS Fundamentals
- [ ] API Input Validation
- [ ] Avoiding Sensitive Data Exposure
6. API Query Features
- [ ] Filtering
- [ ] Search
- [ ] Ordering
- [ ] Pagination
- [ ] Query Parameter Validation
- [ ] Query Optimization
- [ ] API Versioning Fundamentals
7. Error Handling & Documentation
- [ ] Standardized API Error Responses
- [ ] Custom Exception Handler
- [ ] Validation Error Handling
- [ ] Not Found Handling
- [ ] Permission Error Handling
- [ ] OpenAPI Schema
- [ ] Swagger UI
- [ ] ReDoc
- [ ] API Documentation
8. ShopSphere API Development
- [ ] Category APIs
- [ ] Product List API
- [ ] Product Detail API
- [ ] Product Search and Filter API
- [ ] Review APIs
- [ ] Cart APIs
- [ ] Wishlist APIs
- [ ] Coupon APIs
- [ ] Tax and Shipping APIs
- [ ] Checkout API
- [ ] Order APIs
- [ ] Payment APIs
- [ ] Invoice APIs
- [ ] Admin Management APIs
Output
- [ ] Complete ShopSphere REST API
- [ ] Reusable Serializers and API Views
- [ ] Secure API Permissions
- [ ] Filtering, Searching, and Pagination
- [ ] Documented APIs

---

## 🟢 Milestone 11 — JWT Authentication

**Status:** ⬜ Not Started

### Topics

1. JWT Fundamentals
- [ ] What Is JSON Web Token (JWT)?
- [ ] JWT Structure
- [ ] Header
- [ ] Payload
- [ ] Signature
- [ ] Signing vs Encryption
- [ ] Access Token
- [ ] Refresh Token
- [ ] Token-Based Authentication Flow
2. Simple JWT Integration
- [ ] Install and Configure Simple JWT
- [ ] Token Obtain Endpoint
- [ ] Token Refresh Endpoint
- [ ] Token Verify Endpoint
- [ ] Access Token Lifetime
- [ ] Refresh Token Lifetime
- [ ] Token Rotation
- [ ] Refresh Token Blacklisting
- [ ] Logout Flow
3. Protecting APIs
- [ ] JWT Authentication Class
- [ ] Protected Endpoints
- [ ] Anonymous vs Authenticated Access
- [ ] Authenticated User Context
- [ ] Role-Based API Authorization
- [ ] Object-Level API Permissions
- [ ] Custom Permission Integration
4. JWT Security
- [ ] Token Expiration
- [ ] Refresh Token Protection
- [ ] Token Storage Considerations
- [ ] HTTPS Requirement in Production
- [ ] Secure Cookie Considerations
- [ ] XSS and CSRF Trade-offs
- [ ] Secret Key Management
- [ ] Token Revocation
- [ ] Brute-Force Protection
- [ ] Authentication Error Handling
5. JWT Testing
- [ ] Token Obtain Tests
- [ ] Token Refresh Tests
- [ ] Expired Token Tests
- [ ] Invalid Token Tests
- [ ] Blacklisted Token Tests
- [ ] Protected API Tests
- [ ] Role-Based Access Tests
Output
- [ ] JWT Authentication System
- [ ] Protected REST APIs
- [ ] Refresh and Logout Flow
- [ ] Role-Based API Authorization
- [ ] JWT Security Tests

---

## 🟢 Milestone 12 — Testing

**Status:** ⬜ Not Started

### Topics

1. Testing Fundamentals
- [ ] Software Testing Fundamentals
- [ ] Unit Testing
- [ ] Integration Testing
- [ ] Functional Testing
- [ ] Regression Testing
- [ ] Test Coverage
- [ ] Test Pyramid
- [ ] Test Fixtures
- [ ] Arrange-Act-Assert Pattern
- [ ] Test-Driven Development (TDD) Introduction
2. Django Testing
- [ ] Django Test Framework
- [ ] SimpleTestCase
- [ ] TestCase
- [ ] TransactionTestCase
- [ ] Test Client
- [ ] Model Testing
- [ ] Form Testing
- [ ] View Testing
- [ ] URL Testing
- [ ] Template / Response Testing
- [ ] Authentication Testing
- [ ] Authorization Testing
3. Service & Database Testing
- [ ] Service Function Testing
- [ ] Business Rule Testing
- [ ] Database Constraint Testing
- [ ] Transaction Testing
- [ ] Rollback Testing
- [ ] Signal Testing
- [ ] on_commit() Testing
- [ ] Concurrency Testing Fundamentals
- [ ] Inventory Consistency Testing
4. Integration Testing
- [ ] Registration and Login
- [ ] Product Management
- [ ] File Upload and Cleanup
- [ ] Review Workflow
- [ ] RBAC and Object Permissions
- [ ] Inventory Workflow
- [ ] Cart and Wishlist
- [ ] Checkout Workflow
- [ ] Order Processing
- [ ] Payment Workflow
- [ ] Coupon Validation
- [ ] Invoice Generation
- [ ] Cancellation and Stock Restoration
- [ ] Refund Workflow (When Implemented)
5. API Testing
- [ ] DRF APIClient
- [ ] Serializer Testing
- [ ] APIView Testing
- [ ] Generic View Testing
- [ ] ViewSet Testing
- [ ] Router / URL Testing
- [ ] API Permission Testing
- [ ] JWT Authentication Testing
- [ ] Pagination Testing
- [ ] Filtering and Search Testing
- [ ] API Error Response Testing
6. External Service & Background Task Testing
- [ ] Mocking Fundamentals
- [ ] Mock External API Calls
- [ ] Payment Callback / IPN Testing
- [ ] Idempotency Testing
- [ ] Duplicate Request Testing
- [ ] Email Testing
- [ ] Celery Task Testing
- [ ] Retry and Failure Testing
- [ ] WebSocket Testing
- [ ] Delivery Tracking Testing
7. Testing Tools
- [ ] pytest Fundamentals
- [ ] pytest-django
- [ ] Factory Boy
- [ ] Coverage.py
- [ ] Postman
- [ ] Test Data Management
- [ ] Continuous Test Execution
8. Quality & Regression
- [ ] Run Full Test Suite
- [ ] Identify and Fix Regressions
- [ ] Review Test Coverage
- [ ] Remove Fragile Tests
- [ ] Test Critical Permission Boundaries
- [ ] Test Failure and Recovery Paths
- [ ] Document Test Commands and Results
Output
- [ ] Complete Automated Test Suite
- [ ] Unit and Integration Test Coverage
- [ ] API Test Coverage
- [ ] Transaction and Payment Test Coverage
- [ ] Regression Testing Workflow

---

## 🟢 Milestone 13 — Delivery Management & Live GPS Tracking
1. Delivery Management
- [ ] Deliveries App Setup
- [ ] Delivery Model
- [ ] Rider Management
- [ ] Rider Profile
- [ ] Rider Assignment
- [ ] Delivery Status Management
- [ ] Tracking ID Generation
- [ ] Delivery History
- [ ] Delivery Permission Rules
- [ ] Delivery Workflow Testing
2. GPS & Location Tracking
- [ ] Browser Geolocation API
- [ ] Latitude and Longitude
- [ ] Requesting Location Permission
- [ ] GPS Location Collection
- [ ] Rider Location Update API
- [ ] Location Storage
- [ ] Location Update Validation
- [ ] Location Update Frequency
- [ ] Customer Tracking Page
- [ ] Delivery Tracking URL
- [ ] Location Privacy and Access Control
3. Map & ETA Integration
- [ ] Map API Fundamentals
- [ ] Map Integration
- [ ] Geocoding
- [ ] Reverse Geocoding
- [ ] Map Markers
- [ ] Rider Location on Map
- [ ] Delivery Destination on Map
- [ ] Route Display
- [ ] Distance Calculation
- [ ] Estimated Time of Arrival (ETA)
- [ ] API Usage Limits and Key Protection
4. Background Processing --- Celery
- [ ] Synchronous vs Asynchronous Processing
- [ ] Background Task Fundamentals
- [ ] Celery Architecture
- [ ] Redis as Message Broker
- [ ] Celery Installation
- [ ] Celery Configuration
- [ ] Celery Application Setup
- [ ] Celery Tasks
- [ ] Celery Workers
- [ ] Task Queue Fundamentals
- [ ] Task Scheduling
- [ ] Celery Beat
- [ ] Task Retry
- [ ] Task Failure Handling
- [ ] Task Timeouts
- [ ] Idempotent Tasks
- [ ] Task Monitoring
- [ ] Post-Commit Task Dispatch
5. Real-Time Communication
- [ ] ASGI Fundamentals
- [ ] WSGI vs ASGI
- [ ] Django Channels
- [ ] WebSocket Fundamentals
- [ ] HTTP vs WebSocket
- [ ] Channels Installation
- [ ] WebSocket Consumers
- [ ] WebSocket Routing
- [ ] Channel Layers
- [ ] Redis Channel Layer
- [ ] WebSocket Authentication
- [ ] Connection Lifecycle
- [ ] Real-Time Location Updates
- [ ] Customer Live Tracking Interface
- [ ] Reconnection and Failure Handling
6. Notification System
- [ ] Notifications App Setup
- [ ] Notification Model
- [ ] Notification Templates
- [ ] In-App Notifications
- [ ] Order Confirmation Notification
- [ ] Payment Confirmation Notification
- [ ] Order Status Notifications
- [ ] Rider Assignment Notification
- [ ] Out-for-Delivery Notification
- [ ] Delivery Confirmation Notification
- [ ] Email Integration
- [ ] SMS Gateway Integration
- [ ] WhatsApp Business API Integration
- [ ] Background Notification Tasks
- [ ] Notification Retry and Failure Handling
- [ ] Notification Preferences and Access Control
7. Integration & Testing
- [ ] Order-to-Delivery Workflow
- [ ] Rider Assignment Workflow
- [ ] GPS Update API Testing
- [ ] WebSocket Integration Testing
- [ ] Celery Task Testing
- [ ] Notification Delivery Testing
- [ ] Location Privacy Testing
- [ ] Failure and Recovery Testing
Output
- [ ] Delivery Management System
- [ ] Rider Assignment System
- [ ] GPS-Based Delivery Tracking
- [ ] Real-Time WebSocket Updates
- [ ] Celery Background Processing
- [ ] Automated Notification System

---

## 🟢 Milestone 14 — Production Deployment & DevOps

**Status:** ⬜ Not Started

### Topics
1. Linux & Server Management
- [ ] Linux Server Fundamentals
- [ ] VPS / Server Setup
- [ ] SSH Configuration
- [ ] SSH Key Authentication
- [ ] Linux Users and Groups
- [ ] File and Directory Permissions
- [ ] Process Management
- [ ] Service Management (systemd)
- [ ] Package Management
- [ ] Environment Configuration
- [ ] Firewall Fundamentals
- [ ] Server Security Basics
2. Django Production Configuration
- [ ] Development vs Production Settings
- [ ] Environment Variables
- [ ] .env Management
- [ ] DEBUG=False
- [ ] ALLOWED_HOSTS
- [ ] CSRF_TRUSTED_ORIGINS
- [ ] Secret Key Management
- [ ] Static Files Configuration
- [ ] Media Files Configuration
- [ ] Production Database Configuration
- [ ] Logging Configuration
- [ ] Error Handling
- [ ] Django Deployment Checklist
- [ ] Production Security Settings
3. Application & Web Servers
- [ ] WSGI Fundamentals
- [ ] ASGI Fundamentals
- [ ] Gunicorn
- [ ] Uvicorn
- [ ] Nginx
- [ ] Reverse Proxy
- [ ] Application Server Configuration
- [ ] Static and Media Serving
- [ ] Domain Configuration
- [ ] DNS Fundamentals
- [ ] HTTPS / SSL Configuration
- [ ] WebSocket Proxy Configuration
4. Docker & Containerization
- [ ] Container Fundamentals
- [ ] Docker Installation
- [ ] Docker Images
- [ ] Docker Containers
- [ ] Dockerfile
- [ ] Docker Build
- [ ] Docker Compose
- [ ] Docker Volumes
- [ ] Docker Networks
- [ ] Environment Variables in Containers
- [ ] Django Container
- [ ] PostgreSQL Container
- [ ] Redis Container
- [ ] Celery Worker Container
- [ ] Celery Beat Container
- [ ] Container Logs
- [ ] Health Checks
- [ ] Development vs Production Compose Configuration
5. CI/CD & Automation
- [ ] CI/CD Fundamentals
- [ ] Continuous Integration
- [ ] Continuous Delivery / Deployment
- [ ] GitHub Actions Fundamentals
- [ ] Automated Test Workflow
- [ ] Lint / Quality Check Workflow
- [ ] Build Pipeline
- [ ] Deployment Pipeline
- [ ] Environment Separation
- [ ] Secrets Management
- [ ] Deployment Failure Handling
6. Production Operations
- [ ] VPS Deployment
- [ ] Database Deployment
- [ ] Application Deployment
- [ ] Static File Deployment
- [ ] Media Storage Strategy
- [ ] Domain and HTTPS Setup
- [ ] Celery Worker Deployment
- [ ] Celery Beat Deployment
- [ ] Redis Deployment
- [ ] Production Smoke Testing
- [ ] Monitoring Fundamentals
- [ ] Application and Server Logs
- [ ] Error Monitoring
- [ ] Database Backup
- [ ] Backup Restore Drill
- [ ] Recovery Planning
- [ ] Update and Rollback Procedure
7. Final Production Verification
- [ ] DEBUG=False Verified
- [ ] Secrets Not Committed to Git
- [ ] HTTPS Verified
- [ ] Authentication and Permissions Verified
- [ ] Payment Sandbox / Live Readiness Reviewed
- [ ] Database Backup Verified
- [ ] Static and Media Files Verified
- [ ] Background Tasks Verified
- [ ] WebSocket Verified (if deployed)
- [ ] Automated Tests Passing
- [ ] Logs and Error Monitoring Working
- [ ] Deployment Documentation Complete
Output
- [ ] Dockerized ShopSphere
- [ ] Production Server Configuration
- [ ] CI/CD Pipeline
- [ ] Background Task Deployment
- [ ] Secure HTTPS Deployment
- [ ] Backup and Recovery Procedure
- [ ] Production-Oriented E-commerce Backend

---

## 5. Cross-Milestone Engineering Standards
These practices apply throughout the project, not only in one milestone.

Git & GitHub
- Use meaningful commits.
- Keep the repository clean.
- Never commit .env, secrets, private keys, or production
  credentials.
- Update documentation with important features and setup changes.
- Use branches for larger or risky changes when appropriate.
Linux & Bash
- Practice commands in the WSL2 Ubuntu development environment.
- Understand paths, permissions, processes, services, logs, and
  package management.
- Keep useful development commands documented.
Security
- Enforce authentication and authorization on protected operations.
- Validate all user-controlled input.
- Check object ownership and role permissions.
- Protect uploaded files and sensitive data.
- Keep payment verification server-side.
- Avoid exposing secrets or internal errors.
- Use HTTPS in production.
- Apply rate limits where appropriate.
Database Integrity
- Use database constraints for rules that must hold at the database
  level.
- Use transactions for related writes that must succeed or fail
  together.
- Consider concurrent requests and race conditions.
- Optimize queries based on measurement, not guesswork.
- Back up data and verify that restoration works.
Testing
- Add tests as each feature is implemented.
- Test success, failure, invalid input, permissions, and boundary
  cases.
- Test critical business workflows and external service failure paths.
- Run the relevant test suite before merging or deploying.
Documentation
- Document setup and environment variables.
- Explain important architecture decisions.
- Record migration and backup procedures.
- Document API endpoints and expected responses.
- Keep known limitations and deferred work visible.

---

# 📁 6. Target Project Structure

The following is the planned final project structure. Applications and configuration files will be added as development progresses.

```text
ShopSphere/
│
├── accounts/
├── categories/
├── products/
├── reviews/
├── inventory/
├── carts/
├── wishlist/
├── taxes/
├── shipping/
├── orders/
├── payments/
├── deliveries/
├── notifications/
├── api/
│
├── templates/
├── static/
├── media/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── manage.py

```

---

## 🚀 7. Final Project Vision
By completing the roadmap, ShopSphere should demonstrate the ability to:
- Build and maintain a Django application with clear architecture.
- Model e-commerce entities and relationships.
- Implement authentication, authorization, and role-based access.
- Design reliable cart, checkout, order, inventory, and payment
  workflows.
- Work confidently with PostgreSQL and Django ORM performance.
- Design and document REST APIs.
- Secure APIs with JWT authentication.
- Test business logic, permissions, transactions, and integrations.
- Build asynchronous and real-time features.
- Deploy and operate a Django application using production-oriented
  tools.
- Explain technical decisions, trade-offs, and failure handling.
Important: This final vision describes the intended outcome of the
roadmap. It must not be copied into the project's README as a list of
already completed capabilities.

**From Django Fundamentals to Production-Oriented Backend Engineering.**

---

