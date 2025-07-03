# **Software Requirements Specification (SRS)**

## **Project Aether: Unified SEO Intelligence Platform**

Version: 2.1 (Detailed Architecture)  
Date: July 2, 2025  
Status: Final

### **1\. Introduction**

#### **1.1. Purpose**

This document provides a comprehensive and detailed specification for **Project Aether**, a proprietary, internal software platform designed to be the single source of truth for SEO analysis and content strategy. The platform addresses the time-intensive and variable nature of manual SEO work by unifying three critical pillars of data:

1. **Live Site Data:** Acquired via a sophisticated, JavaScript-aware web crawler.  
2. **Real-Time Market Data:** Sourced from industry-leading external APIs (e.g., DataForSEO, Google).  
3. **Generative AI Insights:** Powered by Amazon Bedrock's Foundational Models (FMs).

Project Aether will standardize best practices, automate high-effort tasks, and scale the agency's ability to deliver consistent, data-driven SEO outcomes that are grounded in both technical reality and current market dynamics.

#### **1.2. Scope**

The platform will be an internal, web-based SaaS application providing a modular suite of SEO tools.

##### **1.2.1. In-Scope Functionality**

* **Module 1: Live Site Audit & Technical Crawler:** A comprehensive crawler to analyze on-page and technical SEO factors.  
* **Module 2: Performance & Core Web Vitals Analysis:** Integration with Google PageSpeed Insights.  
* **Module 3: Off-Page & Backlink Intelligence:** Integration with a third-party backlink data provider.  
* **Module 4: AI-Powered Keyword & Clustering Engine:** Semantic keyword generation and intent-based grouping.  
* **Module 5: SERP-Driven Content Brief Generator:** AI-powered content planning grounded in live competitor data.  
* **Module 6: Programmatic Schema Markup Generator:** AI-assisted generation of valid JSON-LD schema.  
* **Module 7: AI-Assisted Internal Linking Auditor:** Automated discovery of contextual internal linking opportunities.  
* **Core:** Centralized project/client management and user authentication for employees.

##### **1.2.2. Out-of-Scope Functionality**

* Direct client-facing dashboards or reports.  
* Automated implementation of SEO fixes (e.g., direct publishing to a client's CMS).  
* Billing, subscription, or advanced role-based access control (RBAC).

#### **1.3. Definitions, Acronyms, and Abbreviations**

* **AC:** Acceptance Criteria  
* **Bedrock:** Amazon Bedrock (AWS Managed AI Service)  
* **Boto3:** The AWS SDK for Python  
* **CI/CD:** Continuous Integration / Continuous Deployment  
* **CWV:** Core Web Vitals (LCP, INP, CLS)  
* **FastAPI:** A modern, fast web framework for building APIs with Python  
* **IaC:** Infrastructure as Code  
* **IAM:** Identity and Access Management (AWS)  
* **JSON-LD:** JavaScript Object Notation for Linked Data  
* **ORM:** Object-Relational Mapping  
* **OWASP:** Open Web Application Security Project  
* **SPA:** Single Page Application  
* **SRS:** Software Requirements Specification

### **2\. Overall Description**

#### **2.1. Product Perspective**

Project Aether is a new, standalone internal system. It functions as a SaaS platform for internal use, integrating with the company's Identity Provider (e.g., Google Workspace) for authentication. Its primary backend dependencies are the **Scrapy/Playwright crawling engine**, the **Amazon Bedrock service**, and external data APIs (**Google PageSpeed Insights**, **DataForSEO**, etc.).

#### **2.2. User Personas**

* **Alex, The SEO Analyst:** Uses the platform to automate technical audits, keyword research, and internal link analysis, freeing up time for high-level strategy.  
* **Sarah, The Content Manager:** Uses the platform to generate data-driven, standardized content briefs in minutes, ensuring writers create content that is strategically superior to what is currently ranking.

#### **2.3. General Constraints**

* **Technology Stack:** The backend MUST be Python 3.11+ with FastAPI. The frontend MUST be React 18+ with TypeScript.  
* **Cloud Environment:** The entire system MUST be deployed on AWS within the us-east-1 region.  
* **API Keys:** All external API keys (Bedrock, DataForSEO, etc.) MUST be securely stored using AWS Secrets Manager and must not be exposed in client-side code.  
* **Data Privacy:** No client-identifiable data may be stored in client-side code or logs.  
* **Budget:** API and model usage must be monitored. The system will default to the most cost-effective models and cache API responses aggressively to manage costs.

### **3\. Functional Requirements (FR)**

#### **3.1. FR-1: Live Site Audit & Technical Crawler**

* **User Story:** As an SEO Analyst, I want to initiate a full crawl of a client's website to get a complete and up-to-the-minute inventory of all technical and on-page SEO factors, so I can identify foundational issues.  
* **UI/Logic:** A "Site Management" area will allow users to add a client and initiate a site crawl by providing a root URL. Crawl status (Queued, In Progress, Completed, Failed) must be visible.  
* **Technology:** The crawler will be built using **Scrapy** integrated with the **scrapy-playwright** plugin to ensure accurate rendering and analysis of JavaScript-heavy pages.  
* **Acceptance Criteria:**  
  * AC 1.1: The crawl must be executed as an asynchronous Celery task.  
  * AC 1.2: The crawler must collect URL, HTTP Status Code, Title Tag & length, Meta Description & length, Headers (H1-H6), Word Count, Image alt text presence, Canonical Tag URL, Hreflang attributes, and all internal/external links (including anchor text and nofollow status) for each page.  
  * AC 1.3: The system must generate a filterable and sortable report identifying common issues like broken internal/external links (404s), server errors (5xx), redirect chains, duplicate titles/metas, multiple H1 tags, and missing alt text.  
  * AC 1.4: The system must gracefully handle crawl errors (e.g., timeouts, robots.txt restrictions) and log them without crashing the entire crawl job.

#### **3.2. FR-2: Performance & Core Web Vitals Analysis**

* **User Story:** As an SEO Analyst, I want to see the Core Web Vitals for key pages of a client's site directly within my audit, so I can diagnose performance issues without switching tools.  
* **Logic:** The system will integrate with the **Google PageSpeed Insights API**.  
* **Acceptance Criteria:**  
  * AC 2.1: After a crawl, the system shall automatically fetch and display CWV (LCP, INP, CLS) and overall Performance scores for the homepage and other key pages identified during the crawl.  
  * AC 2.2: The report must be available for both Mobile and Desktop views.

#### **3.3. FR-3: Off-Page & Backlink Intelligence**

* **User Story:** As an SEO Analyst, I want a high-level overview of a client's backlink profile to understand their off-page authority.  
* **Logic:** The system will integrate with a third-party backlink API (e.g., Ahrefs, Semrush, DataForSEO). Users will be required to enter their own API key in a secure settings area.  
* **Acceptance Criteria:**  
  * AC 3.1: The system will pull and display key metrics: Total Backlinks, Total Referring Domains, and a summary of top anchor texts.

#### **3.4. FR-4: AI-Powered Keyword & Clustering Engine**

* **User Story:** As an SEO Analyst, I want to input a primary keyword and receive a list of related keywords automatically grouped by user intent, so I can quickly build a topical authority map.  
* **Logic:** The backend will send a prompt to an **AWS Bedrock** model (e.g., Claude 3 Haiku) requesting keyword generation and semantic clustering in a structured JSON format.  
* **Acceptance Criteria:**  
  * AC 4.1: The UI must provide a single input for a "Head Term".  
  * AC 4.2: Results shall be displayed in expandable sections, with each section title being the name of a semantic cluster (e.g., "Informational Intent," "Commercial Intent").  
  * AC 4.3: An "Export to CSV" button must be available after a successful response.

#### **3.5. FR-5: SERP-Driven Content Brief Generator**

* **User Story:** As a Content Manager, I want to provide a target keyword and have the system analyze the top 10 search results to generate a comprehensive content brief, so I can create content strategically superior to what is currently ranking.  
* **Logic:** This is a multi-step, chained process executed by a Celery worker:  
  1. Call the **DataForSEO SERP API** to get the top 10 organic results, "People Also Ask" (PAA), and "Related Searches."  
  2. Asynchronously scrape the main text content from each of the top 10 URLs.  
  3. Construct a sophisticated prompt for a powerful **AWS Bedrock** model (e.g., Claude 3 Sonnet), providing the target keyword, audience, PAA, related searches, and the full scraped text from competitors as context.  
* **Acceptance Criteria:**  
  * AC 5.1: The UI must show a multi-step loading indicator (Fetching SERP, Analyzing Content, Generating Brief).  
  * AC 5.2: The generated brief must be a detailed, actionable document in a rich text editor, including title suggestions, meta description, a logical heading structure (H2s, H3s), key entities to include, and an FAQ section based on PAA data.  
  * AC 5.3: If the DataForSEO API call fails, the system must return a 502 Bad Gateway error. If scraping fails, the system should inform the user but still attempt to generate a more generic brief.

#### **3.6. FR-6: Programmatic Schema Markup Generator**

* **User Story:** As an SEO Analyst, I want to paste page content and select a schema type to instantly generate valid JSON-LD, so I can implement structured data without manual coding.  
* **Logic:** The backend will send the user's content and selected schema type to an **AWS Bedrock** model, with a prompt instructing it to act as a technical SEO expert and generate a valid, complete JSON-LD script.  
* **Acceptance Criteria:**  
  * AC 6.1: The UI must provide a dropdown to select a schema type (e.g., FAQPage, Article, LocalBusiness, Product, HowTo).  
  * AC 6.2: The output must be a formatted code block with syntax highlighting and a "Copy Script" button.  
  * AC 6.3: If the generated output from the LLM is not valid JSON, the backend should attempt to fix it or return an error.

#### **3.7. FR-7: AI-Assisted Internal Linking Auditor**

* **User Story:** As an SEO Analyst, I want to audit a client's entire crawled site to find contextually relevant internal linking opportunities, so I can improve site architecture.  
* **Logic:** This module relies on the output of the **Live Site Crawler (FR-1)**.  
  1. The user selects a "Target Page" they want to build links *to*.  
  2. The system iterates through all other crawled pages ("Source Pages").  
  3. For each Source Page, it prompts an **AWS Bedrock** model with its text and the topic of the Target Page, instructing it to find the most relevant phrase for an anchor text and return the surrounding sentence for context.  
* **Acceptance Criteria:**  
  * AC 7.1: Results shall be displayed in a data table with "Source URL," "Suggested Anchor Text," and "Context Snippet."  
  * AC 7.2: The UI must allow the user to set the state of a suggestion to Pending, Completed, or Dismissed, with changes saved automatically.  
  * AC 7.3: The system must not suggest linking a page to itself or suggest a link where one already exists between the source and target.

### **4\. System Architecture & Detailed Technology Stack**

This section details the specific technologies, libraries, and architectural patterns to be used in the construction of Project Aether.

#### **4.1. Backend Architecture**

The backend is a decoupled service-oriented architecture designed for scalability and maintainability.

* **Language:** **Python 3.11+**  
  * *Rationale:* Chosen for its mature data science ecosystem, extensive support for web technologies, and first-class AI/ML library support.  
* **Web Framework:** **FastAPI**  
  * *Rationale:* Provides high performance comparable to NodeJS and Go due to its asynchronous nature (built on Starlette and Uvicorn). Its automatic data validation via **Pydantic** models reduces boilerplate and runtime errors. Dependency Injection system promotes clean, testable code.  
  * *Key Libraries:*  
    * **Pydantic V2:** For data validation, settings management, and serialization.  
    * **Uvicorn:** As the lightning-fast ASGI server for development.  
    * **Gunicorn:** As a process manager for Uvicorn in production, enabling multi-worker deployments to utilize all available CPU cores.  
* **Asynchronous Task Queue:** **Celery**  
  * *Rationale:* Essential for offloading long-running, resource-intensive tasks like website crawls and multi-step AI analyses from the main API thread, ensuring the UI remains responsive.  
  * *Components:*  
    * **Broker:** **Redis** (via AWS ElastiCache) will be used as the message broker for its speed and simplicity.  
    * **Result Backend:** **PostgreSQL** will be used to store task state and results, allowing for persistent tracking of job statuses.  
* **Crawler Engine:** **Scrapy** with **scrapy-playwright**  
  * *Rationale:* Scrapy is a highly optimized and extensible crawling framework. The integration with Playwright is critical for accurately rendering and analyzing modern, JavaScript-heavy websites, which is a common failure point for simpler crawlers.  
  * *Implementation:* Scrapy projects will be structured as independent modules. Celery tasks will invoke Scrapy crawls programmatically via its internal API.  
* **Database Interaction (ORM):** **SQLAlchemy 2.0** with **asyncpg**  
  * *Rationale:* SQLAlchemy is the de-facto standard ORM in the Python world. Version 2.0's native asyncio support, when paired with the asyncpg driver, allows for fully non-blocking database operations, which is critical for performance in an async framework like FastAPI.  
  * *Migrations:* **Alembic** will be used to manage and version control the database schema, ensuring repeatable and safe database updates.  
* **AI Service Integration:** **AWS Boto3 SDK**  
  * *Rationale:* The official AWS SDK for Python provides direct, secure access to AWS services.  
  * *Client:* The bedrock-runtime client will be used specifically for invoking foundation models.  
* **Dependency Management:** **Poetry**  
  * *Rationale:* Provides deterministic dependency resolution (poetry.lock), virtual environment management, and packaging, ensuring consistent environments from development to production.

#### **4.2. Frontend Architecture**

The frontend is a modern Single Page Application (SPA) focused on a highly interactive and responsive user experience.

* **Framework:** **React 18+** with **TypeScript**  
  * *Rationale:* React's component-based model and vast ecosystem are ideal for building complex UIs. TypeScript adds static typing, significantly reducing runtime errors and improving developer experience and code maintainability.  
* **Build Tool:** **Vite**  
  * *Rationale:* Offers near-instantaneous hot module replacement (HMR) and significantly faster cold starts compared to older tools like Webpack, dramatically improving developer productivity.  
* **State Management:** **Zustand**  
  * *Rationale:* A simple, unopinionated, and powerful state management library. It avoids the boilerplate of Redux while providing a clean, hook-based API that is easy to integrate into a React application.  
* **Data Fetching & Server State:** **TanStack Query (React Query)**  
  * *Rationale:* Essential for managing server state. It handles caching, background refetching, and deduplication of requests out of the box, simplifying data fetching logic and improving perceived performance.  
* **UI Components:** **Shadcn/UI** & **Tailwind CSS**  
  * *Rationale:* This combination provides the best of both worlds. **Tailwind CSS** is a utility-first CSS framework for rapid styling. **Shadcn/UI** is not a traditional component library; instead, it provides beautifully designed, accessible, and unstyled components (built with Radix UI and Tailwind CSS) that can be copied directly into the project, offering maximum control and customizability.  
* **Data Visualization:** **Recharts**  
  * *Rationale:* A composable charting library built on React components, making it easy to create beautiful and interactive charts to display audit data.

#### **4.3. Datastores**

* **Primary Database:** **PostgreSQL 15+** (via AWS RDS)  
  * *Rationale:* A powerful, reliable, and open-source relational database. Its robust support for the JSONB data type is perfect for storing unstructured or semi-structured responses from external APIs without needing a separate NoSQL database.  
* **Cache & Message Broker:** **Redis** (via AWS ElastiCache)  
  * *Rationale:* An in-memory data store used for two critical purposes: (1) as the high-speed message broker for Celery, and (2) as a general-purpose application cache for frequently accessed data that doesn't need to hit the primary database.

#### **4.4. DevOps & Infrastructure**

* **Cloud Provider:** **Amazon Web Services (AWS)**  
* **Infrastructure as Code (IaC):** **AWS CDK (Cloud Development Kit)** with TypeScript  
  * *Rationale:* Allows the team to define all cloud infrastructure (VPCs, databases, compute services, IAM roles) in a familiar programming language, enabling version control, peer review, and automated, repeatable deployments.  
* **Containerization:** **Docker** & **Docker Compose**  
  * *Rationale:* Docker provides consistent environments across the entire lifecycle. Docker Compose will be used to orchestrate multi-container setups (API, workers, database) for local development.  
* **Compute Services:**  
  * **API Service (FastAPI):** **AWS App Runner**. *Rationale:* A fully managed service that is ideal for web APIs. It handles load balancing, auto-scaling, and deployments directly from a container image, simplifying operations.  
  * **Async Workers (Celery):** **AWS ECS Fargate**. *Rationale:* A serverless compute engine for containers. It's perfect for running background tasks, as it can scale the number of worker containers up or down based on the number of tasks in the queue.  
* **CI/CD Pipeline:** **GitHub Actions**  
  * *Rationale:* Tightly integrated with the source code repository. The pipeline will automate linting, testing, container building, and deployment to AWS environments (staging and production).  
* **Secure Storage:** **AWS Secrets Manager**  
  * *Rationale:* The designated service for storing and rotating all sensitive credentials, such as database passwords and external API keys. The application will fetch these secrets at runtime via IAM roles, never hardcoding them.  
* **Logging & Monitoring:** **AWS CloudWatch**  
  * *Rationale:* The native AWS solution for observability. It will be used to collect structured logs from the application, monitor key performance metrics (CPU/memory usage, API latency), and set up alarms to notify the team of errors or performance degradation.

### **5\. Non-Functional Requirements**

* **Performance:**  
  * P95 latency for synchronous API endpoints (non-AI/crawl) must be **\< 250ms**.  
  * P95 latency for interactive AI-driven API endpoints must be **\< 15 seconds**.  
  * The React SPA's Largest Contentful Paint (LCP) must be **\< 2.5s**.  
* **Security:**  
  * The application must be protected against the OWASP Top 10 vulnerabilities.  
  * All API endpoints must be protected via OIDC token validation.  
  * Infrastructure will be provisioned in a private VPC. The database will not be publicly accessible.  
  * IAM roles will follow the principle of least privilege. The application's compute role will not have permissions beyond what is explicitly required.  
* **Maintainability & Code Quality:**  
  * Code formatting and linting (black/ruff for Python, Prettier/ESLint for TypeScript) are mandatory and will be enforced by a pre-commit hook and the CI pipeline.  
  * A minimum of **80% unit test coverage** is required for all backend business logic.  
  * All public API endpoints must have corresponding integration tests.