import { useEffect, useState } from "react";

import {
  BarChart3,
  TrendingUp,
  ShoppingCart,
  Package,
  Percent,
  MapPin,
  RefreshCw,
} from "lucide-react";

import {
  ResponsiveContainer,
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";


// ============================================================
// API CONFIGURATION
// ============================================================

const API_BASE =
  "https://retailpulse-backend-4dub.onrender.com/api/analytics";

const DASHBOARD_API =
  `${API_BASE}/dashboard`;

const PRODUCTS_API =
  `${API_BASE}/products`;

const CUSTOMERS_API =
  `${API_BASE}/customers`;

const FORECAST_API =
  `${API_BASE}/forecast`;

const ANOMALIES_API =
  `${API_BASE}/anomalies`;


// ============================================================
// APP
// ============================================================

function App() {

  const [data, setData] = useState(null);

  const [products, setProducts] =
    useState([]);

  const [customers, setCustomers] =
    useState([]);

  const [forecast, setForecast] =
    useState(null);

  const [anomalies, setAnomalies] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  const [filters, setFilters] =
    useState({
      year: "All Time",
      region: "All Regions",
      category: "All Categories",
      segment: "All Segments",
    });


  /* ==========================================================
     LOAD DASHBOARD
  ========================================================== */

  useEffect(() => {

    fetchDashboard();

  }, [filters]);


  /* ==========================================================
     LOAD PRODUCTS
  ========================================================== */

  useEffect(() => {

    fetchProducts();
    fetchCustomers();

  }, [filters]);


  /* ==========================================================
     LOAD FORECAST + ANOMALIES
  ========================================================== */

  useEffect(() => {

    fetchForecast();
    fetchAnomalies();

  }, []);


  /* ==========================================================
     FETCH DASHBOARD
  ========================================================== */

  async function fetchDashboard() {

    try {

      setLoading(true);
      setError("");


      const params =
        new URLSearchParams();


      if (
        filters.year !==
        "All Time"
      ) {

        params.set(
          "date_from",
          `${filters.year}-01-01`
        );

        params.set(
          "date_to",
          `${filters.year}-12-31`
        );

      }


      if (
        filters.region !==
        "All Regions"
      ) {

        params.set(
          "region",
          filters.region
        );

      }


      if (
        filters.category !==
        "All Categories"
      ) {

        params.set(
          "category",
          filters.category
        );

      }


      if (
        filters.segment !==
        "All Segments"
      ) {

        params.set(
          "segment",
          filters.segment
        );

      }


      const query =
        params.toString();


      const url =
        query
          ? `${DASHBOARD_API}?${query}`
          : DASHBOARD_API;


      const response =
        await fetch(url);


      if (!response.ok) {

        throw new Error(
          `Dashboard API returned ${response.status}`
        );

      }


      const result =
        await response.json();


      setData(result);

    } catch (err) {

      console.error(
        "Dashboard API error:",
        err
      );

      setError(
        err.message ||
        "Unable to load dashboard"
      );

    } finally {

      setLoading(false);

    }

  }


  /* ==========================================================
     FETCH PRODUCTS
  ========================================================== */

  async function fetchProducts() {

    try {

      const params =
        new URLSearchParams();


      if (filters.year !== "All Time") {

        params.set(
          "date_from",
          `${filters.year}-01-01`
        );

        params.set(
          "date_to",
          `${filters.year}-12-31`
        );

      }


      if (filters.region !== "All Regions") {

        params.set(
          "region",
          filters.region
        );

      }


      if (filters.category !== "All Categories") {

        params.set(
          "category",
          filters.category
        );

      }


      if (filters.segment !== "All Segments") {

        params.set(
          "segment",
          filters.segment
        );

      }


      const query =
        params.toString();


      const url =
        query
          ? `${PRODUCTS_API}?${query}`
          : PRODUCTS_API;


      const response =
        await fetch(url);


      if (!response.ok) {

        throw new Error(
          `Products API returned ${response.status}`
        );

      }


      const result =
        await response.json();


      setProducts(
        Array.isArray(result)
          ? result
          : []
      );

    } catch (err) {

      console.error(
        "Products API error:",
        err
      );

      setProducts([]);

    }

  }


  /* ==========================================================
     FETCH CUSTOMERS
  ========================================================== */

  async function fetchCustomers() {

    try {

      const params =
        new URLSearchParams();


      if (filters.year !== "All Time") {

        params.set(
          "date_from",
          `${filters.year}-01-01`
        );

        params.set(
          "date_to",
          `${filters.year}-12-31`
        );

      }


      if (filters.region !== "All Regions") {

        params.set(
          "region",
          filters.region
        );

      }


      if (filters.category !== "All Categories") {

        params.set(
          "category",
          filters.category
        );

      }


      if (filters.segment !== "All Segments") {

        params.set(
          "segment",
          filters.segment
        );

      }


      const query =
        params.toString();


      const url =
        query
          ? `${CUSTOMERS_API}?${query}`
          : CUSTOMERS_API;


      const response =
        await fetch(url);


      if (!response.ok) {

        throw new Error(
          `Customers API returned ${response.status}`
        );

      }


      const result =
        await response.json();


      setCustomers(
        Array.isArray(result)
          ? result
          : []
      );

    } catch (err) {

      console.error(
        "Customers API error:",
        err
      );

      setCustomers([]);

    }

  }


  /* ==========================================================
     FETCH FORECAST
  ========================================================== */

  async function fetchForecast() {

    try {

      const response =
        await fetch(
          FORECAST_API
        );


      if (!response.ok) {

        throw new Error(
          `Forecast API returned ${response.status}`
        );

      }


      const result =
        await response.json();


      setForecast(result);

    } catch (err) {

      console.error(
        "Forecast API error:",
        err
      );

      setForecast(null);

    }

  }


  /* ==========================================================
     FETCH ANOMALIES
  ========================================================== */

  async function fetchAnomalies() {

    try {

      const response =
        await fetch(
          ANOMALIES_API
        );


      if (!response.ok) {

        throw new Error(
          `Anomaly API returned ${response.status}`
        );

      }


      const result =
        await response.json();


      setAnomalies(
        Array.isArray(result)
          ? result
          : []
      );

    } catch (err) {

      console.error(
        "Anomaly API error:",
        err
      );

      setAnomalies([]);

    }

  }


  /* ==========================================================
     FILTER HELPERS
  ========================================================== */

  function updateFilter(
    name,
    value
  ) {

    setFilters(
      (current) => ({
        ...current,
        [name]: value,
      })
    );

  }


  function resetFilters() {

    setFilters({

      year: "All Time",

      region: "All Regions",

      category:
        "All Categories",

      segment:
        "All Segments",

    });

  }


  /* ==========================================================
     DATA
  ========================================================== */

  const overview =
    data?.overview || {};


  const monthlyRevenue =
    data?.monthly_revenue || [];


  const categories =
    data?.categories || [];


  const regions =
    data?.regions || [];


  const hasFilters =
    filters.year !== "All Time" ||
    filters.region !== "All Regions" ||
    filters.category !== "All Categories" ||
    filters.segment !== "All Segments";


  /* ==========================================================
     RENDER
  ========================================================== */

  return (

    <div className="app">


      {/* ======================================================
          TOP BAR
      ====================================================== */}

      <header className="topbar">

        <div>

          <h1>
            RetailPulse
          </h1>

          <p>
            Business Intelligence Platform
          </p>

        </div>


        <div className="status">

          <span
            className={
              `status-dot ${
                error
                  ? "offline"
                  : ""
              }`
            }
          />

          {error
            ? "API Offline"
            : "Live Data"}

        </div>

      </header>


      <main className="dashboard">


        {/* ==================================================
            HERO
        ================================================== */}

        <section className="hero">

          <div>

            <p className="eyebrow">
              EXECUTIVE OVERVIEW
            </p>


            <h2>
              Retail performance
              <br />
              at a glance.
            </h2>


            <p className="hero-text">

              Monitor revenue,
              profitability, orders
              and regional performance
              from one intelligent
              workspace.

            </p>

          </div>


          <div className="date-badge">

            <span>
              DATA PERIOD
            </span>

            <strong>

              {filters.year ===
              "All Time"
                ? "2023 — 2026"
                : filters.year}

            </strong>

          </div>

        </section>


        {/* ==================================================
            ERROR
        ================================================== */}

        {error && (

          <div className="error-banner">

            Unable to load
            RetailPulse analytics.

            <br />

            {error}

          </div>

        )}


        {/* ==================================================
            FILTERS
        ================================================== */}

        <section className="filters">


          <Filter
            label="DATE RANGE"
            value={filters.year}
            onChange={(value) =>
              updateFilter(
                "year",
                value
              )
            }
            options={[
              "All Time",
              "2026",
              "2025",
              "2024",
              "2023",
            ]}
          />


          <Filter
            label="REGION"
            value={filters.region}
            onChange={(value) =>
              updateFilter(
                "region",
                value
              )
            }
            options={[
              "All Regions",
              "West",
              "East",
              "Central",
              "South",
            ]}
          />


          <Filter
            label="CATEGORY"
            value={filters.category}
            onChange={(value) =>
              updateFilter(
                "category",
                value
              )
            }
            options={[
              "All Categories",
              "Technology",
              "Furniture",
              "Office Supplies",
            ]}
          />


          <Filter
            label="SEGMENT"
            value={filters.segment}
            onChange={(value) =>
              updateFilter(
                "segment",
                value
              )
            }
            options={[
              "All Segments",
              "Consumer",
              "Corporate",
              "Home Office",
            ]}
          />


          <button
            className={
              `reset-button ${
                hasFilters
                  ? "active"
                  : ""
              }`
            }
            onClick={
              resetFilters
            }
          >

            <RefreshCw
              size={16}
            />

            Reset

          </button>

        </section>


        {/* ==================================================
            KPI CARDS
        ================================================== */}

        <section className="kpi-grid">


          <KpiCard
            icon={
              <TrendingUp
                size={21}
              />
            }
            label="TOTAL REVENUE"
            value={
              loading
                ? "..."
                : formatCurrency(
                    overview.total_revenue
                  )
            }
            accent="revenue"
          />


          <KpiCard
            icon={
              <BarChart3
                size={21}
              />
            }
            label="TOTAL PROFIT"
            value={
              loading
                ? "..."
                : formatCurrency(
                    overview.total_profit
                  )
            }
            accent="profit"
          />


          <KpiCard
            icon={
              <ShoppingCart
                size={21}
              />
            }
            label="TOTAL ORDERS"
            value={
              loading
                ? "..."
                : formatNumber(
                    overview.total_orders
                  )
            }
            accent="orders"
          />


          <KpiCard
            icon={
              <Package
                size={21}
              />
            }
            label="UNITS SOLD"
            value={
              loading
                ? "..."
                : formatNumber(
                    overview.total_units
                  )
            }
            accent="units"
          />


          <KpiCard
            icon={
              <Percent
                size={21}
              />
            }
            label="PROFIT MARGIN"
            value={
              loading
                ? "..."
                : `${overview.profit_margin ?? 0}%`
            }
            accent="margin"
          />

        </section>


        {/* ==================================================
            CHART GRID
        ================================================== */}

        <section className="chart-grid">


          {/* ==================================================
              REVENUE
          ================================================== */}

          <div className="panel large-panel">

            <div className="panel-heading">

              <div>

                <span className="panel-label">
                  REVENUE ANALYTICS
                </span>

                <h3>
                  Revenue & Profit Trend
                </h3>

              </div>


              <TrendingUp
                size={20}
              />

            </div>


            <div className="real-chart">

              {loading ? (

                <div className="chart-loading">
                  Loading revenue analytics...
                </div>

              ) : monthlyRevenue.length === 0 ? (

                <div className="chart-loading">
                  No data available
                  for these filters.
                </div>

              ) : (

                <ResponsiveContainer
                  width="100%"
                  height={560}
                >

                  <AreaChart
                    data={
                      monthlyRevenue
                    }
                    margin={{
                      top: 20,
                      right: 20,
                      left: 0,
                      bottom: 10,
                    }}
                  >

                    <CartesianGrid
                      strokeDasharray="3 3"
                      stroke="rgba(255,255,255,0.06)"
                    />


                    <XAxis
                      dataKey="month"
                      tick={{
                        fill: "#718091",
                        fontSize: 11,
                      }}
                      tickLine={false}
                      axisLine={false}
                    />


                    <YAxis
                      tick={{
                        fill: "#718091",
                        fontSize: 11,
                      }}
                      tickLine={false}
                      axisLine={false}
                      tickFormatter={
                        formatCompactCurrency
                      }
                    />


                    <Tooltip
                      contentStyle={{
                        background:
                          "#0c1923",
                        border:
                          "1px solid rgba(255,255,255,0.1)",
                        borderRadius:
                          "10px",
                        color:
                          "#e8edf5",
                      }}
                      formatter={(value) =>
                        formatCurrency(
                          value
                        )
                      }
                    />


                    <Area
                      type="monotone"
                      dataKey="revenue"
                      stroke="#65bfd1"
                      fill="rgba(101,191,209,0.12)"
                      strokeWidth={2}
                      name="Revenue"
                    />


                    <Area
                      type="monotone"
                      dataKey="profit"
                      stroke="#72d1ae"
                      fill="rgba(114,209,174,0.05)"
                      strokeWidth={2}
                      name="Profit"
                    />

                  </AreaChart>

                </ResponsiveContainer>

              )}

            </div>

          </div>


          {/* ==================================================
              CATEGORY
          ================================================== */}

          <div className="panel">

            <div className="panel-heading">

              <div>

                <span className="panel-label">
                  PERFORMANCE
                </span>

                <h3>
                  Categories
                </h3>

              </div>

            </div>


            <div className="real-chart small-chart">

              {loading ? (

                <div className="chart-loading">
                  Loading categories...
                </div>

              ) : categories.length === 0 ? (

                <div className="chart-loading">
                  No category data.
                </div>

              ) : (

                <ResponsiveContainer
                  width="100%"
                  height={270}
                >

                  <BarChart
                    data={categories}
                    layout="vertical"
                    margin={{
                      top: 10,
                      right: 20,
                      left: 10,
                      bottom: 10,
                    }}
                  >

                    <CartesianGrid
                      strokeDasharray="3 3"
                      stroke="rgba(255,255,255,0.05)"
                      horizontal={false}
                    />


                    <XAxis
                      type="number"
                      tick={{
                        fill: "#718091",
                        fontSize: 10,
                      }}
                      tickLine={false}
                      axisLine={false}
                      tickFormatter={
                        formatCompactCurrency
                      }
                    />


                    <YAxis
                      type="category"
                      dataKey="category"
                      width={95}
                      tick={{
                        fill: "#aab6c4",
                        fontSize: 10,
                      }}
                      tickLine={false}
                      axisLine={false}
                    />


                    <Tooltip
                      contentStyle={{
                        background:
                          "#0c1923",
                        border:
                          "1px solid rgba(255,255,255,0.1)",
                        borderRadius:
                          "10px",
                      }}
                      formatter={(value) =>
                        formatCurrency(
                          value
                        )
                      }
                    />


                    <Bar
                      dataKey="revenue"
                      fill="#65bfd1"
                      radius={[
                        0,
                        5,
                        5,
                        0,
                      ]}
                      name="Revenue"
                    />

                  </BarChart>

                </ResponsiveContainer>

              )}

            </div>

          </div>


          {/* ==================================================
              REGION
          ================================================== */}

          <div className="panel">

            <div className="panel-heading">

              <div>

                <span className="panel-label">
                  GEOGRAPHY
                </span>

                <h3>
                  Regional Performance
                </h3>

              </div>


              <MapPin
                size={20}
              />

            </div>


            <div className="real-chart small-chart">

              {loading ? (

                <div className="chart-loading">
                  Loading regions...
                </div>

              ) : regions.length === 0 ? (

                <div className="chart-loading">
                  No regional data.
                </div>

              ) : (

                <ResponsiveContainer
                  width="100%"
                  height={270}
                >

                  <BarChart
                    data={regions}
                    margin={{
                      top: 10,
                      right: 10,
                      left: 0,
                      bottom: 10,
                    }}
                  >

                    <CartesianGrid
                      strokeDasharray="3 3"
                      stroke="rgba(255,255,255,0.05)"
                      vertical={false}
                    />


                    <XAxis
                      dataKey="region"
                      tick={{
                        fill: "#718091",
                        fontSize: 10,
                      }}
                      tickLine={false}
                      axisLine={false}
                    />


                    <YAxis
                      tick={{
                        fill: "#718091",
                        fontSize: 10,
                      }}
                      tickLine={false}
                      axisLine={false}
                      tickFormatter={
                        formatCompactCurrency
                      }
                    />


                    <Tooltip
                      contentStyle={{
                        background:
                          "#0c1923",
                        border:
                          "1px solid rgba(255,255,255,0.1)",
                        borderRadius:
                          "10px",
                      }}
                      formatter={(value) =>
                        formatCurrency(
                          value
                        )
                      }
                    />


                    <Bar
                      dataKey="revenue"
                      fill="#72d1ae"
                      radius={[
                        5,
                        5,
                        0,
                        0,
                      ]}
                      name="Revenue"
                    />

                  </BarChart>

                </ResponsiveContainer>

              )}

            </div>

          </div>

        </section>


        {/* ==================================================
            PRODUCT PERFORMANCE
        ================================================== */}

        <section className="panel product-panel">

          <div className="panel-heading">

            <div>

              <span className="panel-label">
                PRODUCT INTELLIGENCE
              </span>

              <h3>
                Top Products by Revenue
              </h3>

            </div>


            <Package
              size={20}
            />

          </div>


          <div className="product-table-wrapper">

            {products.length === 0 ? (

              <div className="chart-loading">

                {loading
                  ? "Loading product performance..."
                  : "No product data available."}

              </div>

            ) : (

              <table className="product-table">

                <thead>

                  <tr>

                    <th>
                      #
                    </th>

                    <th>
                      PRODUCT
                    </th>

                    <th>
                      CATEGORY
                    </th>

                    <th>
                      REVENUE
                    </th>

                    <th>
                      PROFIT
                    </th>

                    <th>
                      UNITS
                    </th>

                  </tr>

                </thead>


                <tbody>

                  {products.map(
                    (
                      product,
                      index
                    ) => (

                      <tr
                        key={
                          product.product_id
                        }
                      >

                        <td className="rank">
                          {index + 1}
                        </td>


                        <td>

                          <div className="product-name">

                            {
                              product.product_name
                            }

                          </div>


                          <div className="product-id">

                            {
                              product.product_id
                            }

                          </div>

                        </td>


                        <td>

                          <span className="category-tag">

                            {
                              product.category
                            }

                          </span>

                        </td>


                        <td className="number-cell">

                          {formatCurrency(
                            product.revenue
                          )}

                        </td>


                        <td className="number-cell profit-value">

                          {formatCurrency(
                            product.profit
                          )}

                        </td>


                        <td className="number-cell">

                          {formatNumber(
                            product.units
                          )}

                        </td>

                      </tr>

                    )
                  )}

                </tbody>

              </table>

            )}

          </div>

        </section>


        {/* ==================================================
            CUSTOMER PERFORMANCE
        ================================================== */}

        <section className="panel product-panel">

          <div className="panel-heading">

            <div>

              <span className="panel-label">
                CUSTOMER INTELLIGENCE
              </span>

              <h3>
                Top Customers by Revenue
              </h3>

            </div>


            <ShoppingCart
              size={20}
            />

          </div>


          <div className="product-table-wrapper">

            {customers.length === 0 ? (

              <div className="chart-loading">

                Loading customer intelligence...

              </div>

            ) : (

              <table className="product-table">

                <thead>

                  <tr>

                    <th>
                      #
                    </th>

                    <th>
                      CUSTOMER
                    </th>

                    <th>
                      SEGMENT
                    </th>

                    <th>
                      ORDERS
                    </th>

                    <th>
                      REVENUE
                    </th>

                    <th>
                      PROFIT
                    </th>

                  </tr>

                </thead>


                <tbody>

                  {customers.map(
                    (
                      customer,
                      index
                    ) => (

                      <tr
                        key={
                          customer.customer_id
                        }
                      >

                        <td className="rank">
                          {index + 1}
                        </td>


                        <td>

                          <div className="product-name">

                            {
                              customer.customer_name
                            }

                          </div>


                          <div className="product-id">

                            {
                              customer.customer_id
                            }

                          </div>

                        </td>


                        <td>

                          <span className="category-tag">

                            {
                              customer.segment
                            }

                          </span>

                        </td>


                        <td className="number-cell">

                          {
                            customer.orders
                          }

                        </td>


                        <td className="number-cell">

                          {formatCurrency(
                            customer.revenue
                          )}

                        </td>


                        <td className="number-cell profit-value">

                          {formatCurrency(
                            customer.profit
                          )}

                        </td>

                      </tr>

                    )
                  )}

                </tbody>

              </table>

            )}

          </div>

        </section>


        {/* ==================================================
            FORECAST + ANOMALIES
        ================================================== */}

        <section className="chart-grid">


          <div className="panel large-panel">

            <div className="panel-heading">

              <div>

                <span className="panel-label">
                  PREDICTIVE ANALYTICS
                </span>

                <h3>
                  Revenue Forecast
                </h3>

              </div>

              <TrendingUp
                size={20}
              />

            </div>


            <div className="real-chart">

              {!forecast ? (

                <div className="chart-loading">
                  Loading forecast...
                </div>

              ) : (

                <ResponsiveContainer
                  width="100%"
                  height={360}
                >

                  <AreaChart
                    data={[
                      ...(forecast.history || []),

                      ...(forecast.forecast || []).map(
                        item => ({
                          ...item,
                          forecast: item.revenue,
                        })
                      ),
                    ]}
                  >

                    <CartesianGrid
                      strokeDasharray="3 3"
                      stroke="rgba(255,255,255,0.06)"
                    />

                    <XAxis
                      dataKey="month"
                      tick={{
                        fill: "#718091",
                        fontSize: 10,
                      }}
                      tickLine={false}
                      axisLine={false}
                    />

                    <YAxis
                      tick={{
                        fill: "#718091",
                        fontSize: 10,
                      }}
                      tickLine={false}
                      axisLine={false}
                      tickFormatter={
                        formatCompactCurrency
                      }
                    />

                    <Tooltip
                      contentStyle={{
                        background: "#0c1923",
                        border:
                          "1px solid rgba(255,255,255,0.1)",
                        borderRadius: "10px",
                      }}
                      formatter={(value) =>
                        formatCurrency(value)
                      }
                    />

                    <Area
                      type="monotone"
                      dataKey="revenue"
                      stroke="#65bfd1"
                      fill="rgba(101,191,209,0.10)"
                      strokeWidth={2}
                      name="Historical"
                    />

                    <Area
                      type="monotone"
                      dataKey="forecast"
                      stroke="#d5a85b"
                      fill="rgba(213,168,91,0.08)"
                      strokeWidth={2}
                      strokeDasharray="6 4"
                      name="Forecast"
                    />

                  </AreaChart>

                </ResponsiveContainer>

              )}

            </div>

          </div>


          <div className="panel">

            <div className="panel-heading">

              <div>

                <span className="panel-label">
                  RISK MONITOR
                </span>

                <h3>
                  Profit Anomalies
                </h3>

              </div>

              <BarChart3
                size={20}
              />

            </div>


            <div className="anomaly-list">

              {anomalies.length === 0 ? (

                <div className="chart-loading">

                  <span>
                    ✓
                  </span>

                  <p>
                    No major anomalies detected.
                  </p>

                  <small>
                    Monthly profit is within
                    normal variation.
                  </small>

                </div>

              ) : (

                anomalies.map(
                  (item) => (

                    <div
                      className="anomaly-item"
                      key={item.month}
                    >

                      <div>

                        <strong>
                          {item.month}
                        </strong>

                        <span>
                          Profit:{" "}
                          {formatCurrency(
                            item.profit
                          )}
                        </span>

                      </div>


                      <div>

                        <span
                          className={
                            `severity ${item.severity.toLowerCase()}`
                          }
                        >
                          {item.severity}
                        </span>

                        <small>
                          Z-score: {item.z_score}
                        </small>

                      </div>

                    </div>

                  )
                )

              )}

            </div>

          </div>

        </section>


      </main>

    </div>

  );

}


// ============================================================
// FILTER COMPONENT
// ============================================================

function Filter({
  label,
  value,
  onChange,
  options,
}) {

  return (

    <div>

      <label>
        {label}
      </label>


      <select
        value={value}
        onChange={(event) =>
          onChange(
            event.target.value
          )
        }
      >

        {options.map(
          (option) => (

            <option
              key={option}
              value={option}
            >
              {option}
            </option>

          )
        )}

      </select>

    </div>

  );

}


// ============================================================
// KPI CARD
// ============================================================

function KpiCard({
  icon,
  label,
  value,
  accent,
}) {

  return (

    <div
      className={
        `kpi-card ${accent}`
      }
    >

      <div className="kpi-icon">
        {icon}
      </div>


      <div>

        <p>
          {label}
        </p>

        <h3>
          {value}
        </h3>

      </div>

    </div>

  );

}


// ============================================================
// FORMATTERS
// ============================================================

function formatCurrency(value) {

  if (
    value === null ||
    value === undefined ||
    Number.isNaN(
      Number(value)
    )
  ) {

    return "$0";

  }


  return new Intl.NumberFormat(
    "en-US",
    {
      style: "currency",
      currency: "USD",
      maximumFractionDigits: 0,
    }
  ).format(
    Number(value)
  );

}


function formatCompactCurrency(
  value
) {

  if (
    value === null ||
    value === undefined ||
    Number.isNaN(
      Number(value)
    )
  ) {

    return "$0";

  }


  const number =
    Number(value);


  if (
    Math.abs(number) >=
    1000000
  ) {

    return `$${(
      number / 1000000
    ).toFixed(1)}M`;

  }


  if (
    Math.abs(number) >=
    1000
  ) {

    return `$${(
      number / 1000
    ).toFixed(0)}k`;

  }


  return `$${Math.round(
    number
  )}`;

}


function formatNumber(value) {

  if (
    value === null ||
    value === undefined ||
    Number.isNaN(
      Number(value)
    )
  ) {

    return "0";

  }


  return new Intl.NumberFormat(
    "en-US"
  ).format(
    Number(value)
  );

}


export default App;