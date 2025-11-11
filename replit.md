# FlexGuard Dashboard

## Overview

FlexGuard Dashboard is a real-time monitoring and analytics application built with Streamlit that tracks system anomalies, cost savings, and uptime metrics. The application provides interactive visualizations using Plotly, allows users to filter data by date ranges, configure alert thresholds, and generate PDF reports. It's designed to help operations teams monitor system health and optimize resource utilization.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Problem:** Need an interactive, real-time dashboard for monitoring system metrics without building a complex frontend.

**Solution:** Streamlit framework with Plotly for visualizations.

**Rationale:** Streamlit allows rapid development of data-driven web applications using pure Python, eliminating the need for separate HTML/CSS/JavaScript development. Plotly provides interactive, publication-quality graphs that integrate seamlessly with Streamlit.

**Key Components:**
- Wide layout configuration for maximum screen real estate
- Sidebar-based controls for filtering and threshold configuration
- Date range filtering for historical data analysis (default: last 7 days)
- Interactive visualizations for anomaly detection, cost tracking, and uptime monitoring
- Alert threshold configuration with visual indicators:
  - Anomaly intensity threshold with red X markers on heatmap
  - Minimum uptime threshold with red dashed line on uptime graph
- Comparative analysis feature to overlay previous time periods
- Auto-refresh capability for real-time monitoring (5-60 second intervals)
- Data export functionality (CSV and PDF reports)
- Real-time metrics cards displaying alerts and averages

### Backend Architecture

**Problem:** Need persistent storage for time-series data with efficient querying capabilities.

**Solution:** SQLAlchemy ORM with relational database backend.

**Rationale:** SQLAlchemy provides database-agnostic ORM capabilities, making it easy to switch database backends if needed. The declarative base pattern keeps models clean and maintainable.

**Data Models:**
- **AnomalyData**: Tracks spatial anomalies with coordinates (x, y) and intensity measurements over time
- **CostData**: Records cost savings by component over time
- **UptimeData**: Monitors system uptime percentages over time

**Design Patterns:**
- Session management using SQLAlchemy's sessionmaker pattern
- Indexed timestamp columns for efficient time-range queries
- Separate tables for different metric types to optimize query performance

### Data Storage

**Problem:** Need reliable, scalable storage for time-series monitoring data.

**Solution:** Relational database accessed via DATABASE_URL environment variable.

**Rationale:** Relational databases provide ACID compliance and are well-suited for structured time-series data with complex queries. Environment-based configuration allows flexibility in deployment (can use PostgreSQL, MySQL, SQLite, etc.).

**Schema Design:**
- All tables include indexed timestamp columns for time-range filtering
- Primary key auto-increment IDs for unique record identification
- Nullable=False constraints on critical fields ensure data integrity
- Component-based tracking in CostData allows granular cost analysis

### Report Generation

**Problem:** Users need exportable reports for sharing insights with stakeholders.

**Solution:** ReportLab library for PDF generation.

**Rationale:** ReportLab provides programmatic PDF creation with fine-grained control over layout, styling, and content, allowing creation of professional reports directly from dashboard data.

## External Dependencies

### Core Framework
- **Streamlit**: Web application framework for the dashboard UI
- **Plotly**: Interactive visualization library for graphs and charts
  - Uses `plotly.graph_objects` for detailed chart control
  - Uses `plotly.subplots` for multi-panel visualizations

### Database & ORM
- **SQLAlchemy**: ORM and database toolkit
  - Supports multiple database backends via DATABASE_URL
  - Currently configured to work with any SQLAlchemy-compatible database

### Data Processing
- **NumPy**: Numerical computing for data generation and analysis
- **Pandas**: Data manipulation and analysis (used for report generation)

### Report Generation
- **ReportLab**: PDF generation library
  - Creates structured documents with tables, paragraphs, and styling
  - Supports custom styling and formatting

### Environment Configuration
- **DATABASE_URL**: Environment variable that specifies database connection string (required)
  - Format depends on database type (e.g., `postgresql://user:pass@host/db` or `sqlite:///path/to/db.sqlite`)