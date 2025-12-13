"use client"

import type React from "react"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import "./styles.css"

interface Sweet {
  id: number
  name: string
  category: string
  price: number
  quantity: number
}

interface User {
  username: string
  is_staff: boolean
}

export default function SweetShopApp() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [currentView, setCurrentView] = useState<"login" | "register" | "dashboard">("login")
  const [user, setUser] = useState<User | null>(null)
  const [sweets, setSweets] = useState<Sweet[]>([])
  const [filteredSweets, setFilteredSweets] = useState<Sweet[]>([])
  const [searchTerm, setSearchTerm] = useState("")
  const [categoryFilter, setCategoryFilter] = useState("")
  const [minPrice, setMinPrice] = useState("")
  const [maxPrice, setMaxPrice] = useState("")
  const [message, setMessage] = useState({ text: "", type: "" })
  const [showAdminForm, setShowAdminForm] = useState<"add" | "update" | "restock" | null>(null)
  const [selectedSweet, setSelectedSweet] = useState<Sweet | null>(null)
  const router = useRouter()

  // Form states
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    sweetName: "",
    sweetCategory: "",
    sweetPrice: "",
    sweetQuantity: "",
  })

  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

  useEffect(() => {
    const token = localStorage.getItem("access_token")
    const savedUser = localStorage.getItem("user")
    if (token && savedUser) {
      setIsAuthenticated(true)
      setUser(JSON.parse(savedUser))
      setCurrentView("dashboard")
      fetchSweets()
    }
  }, [])

  useEffect(() => {
    filterSweets()
  }, [searchTerm, categoryFilter, minPrice, maxPrice, sweets])

  const filterSweets = () => {
    let filtered = [...sweets]

    if (searchTerm) {
      filtered = filtered.filter(
        (sweet) =>
          sweet.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          sweet.category.toLowerCase().includes(searchTerm.toLowerCase()),
      )
    }

    if (categoryFilter) {
      filtered = filtered.filter((sweet) => sweet.category.toLowerCase() === categoryFilter.toLowerCase())
    }

    if (minPrice) {
      filtered = filtered.filter((sweet) => sweet.price >= Number.parseFloat(minPrice))
    }

    if (maxPrice) {
      filtered = filtered.filter((sweet) => sweet.price <= Number.parseFloat(maxPrice))
    }

    setFilteredSweets(filtered)
  }

  const showMessage = (text: string, type: "success" | "error") => {
    setMessage({ text, type })
    setTimeout(() => setMessage({ text: "", type: "" }), 4000)
  }

  const fetchSweets = async () => {
    const token = localStorage.getItem("access_token")
    try {
      const response = await fetch(`${API_BASE_URL}/api/sweets/`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      if (response.status === 401) {
        handleLogout()
        return
      }

      if (response.ok) {
        const data = await response.json()
        setSweets(data)
      }
    } catch (error) {
      showMessage("Failed to fetch sweets", "error")
    }
  }

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/login/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: formData.username,
          password: formData.password,
        }),
      })

      const data = await response.json()

      if (response.ok) {
        localStorage.setItem("access_token", data.access_token)
        const userData = { username: formData.username, is_staff: data.is_staff || false }
        localStorage.setItem("user", JSON.stringify(userData))
        setUser(userData)
        setIsAuthenticated(true)
        setCurrentView("dashboard")
        showMessage("Login successful!", "success")
        fetchSweets()
      } else {
        showMessage(data.message || "Login failed", "error")
      }
    } catch (error) {
      showMessage("Login failed. Please try again.", "error")
    }
  }

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/register/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: formData.username,
          email: formData.email,
          password: formData.password,
          
        }),
      })

      const data = await response.json()

      if (response.ok) {
        showMessage("Registration successful! Please login.", "success")
        setCurrentView("login")
        setFormData({ ...formData, password: "" })
      } else {
        showMessage(data.message || "Registration failed", "error")
      }
    } catch (error) {
      showMessage("Registration failed. Please try again.", "error")
    }
  }

  const handleLogout = () => {
    localStorage.removeItem("access_token")
    localStorage.removeItem("user")
    setIsAuthenticated(false)
    setUser(null)
    setCurrentView("login")
    setSweets([])
    showMessage("Logged out successfully", "success")
  }

  const handlePurchase = async (sweetId: number) => {
    const token = localStorage.getItem("access_token")
    try {
      const response = await fetch(`${API_BASE_URL}/api/sweets/${sweetId}/purchase/`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      if (response.status === 401) {
        handleLogout()
        return
      }

      if (response.ok) {
        showMessage("Purchase successful!", "success")
        fetchSweets()
      } else {
        const data = await response.json()
        showMessage(data.message || "Purchase failed", "error")
      }
    } catch (error) {
      showMessage("Purchase failed. Please try again.", "error")
    }
  }

  const handleAddSweet = async (e: React.FormEvent) => {
    e.preventDefault()
    const token = localStorage.getItem("access_token")
    try {
      const response = await fetch(`${API_BASE_URL}/api/sweets/`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: formData.sweetName,
          category: formData.sweetCategory,
          price: Number.parseFloat(formData.sweetPrice),
          quantity: Number.parseInt(formData.sweetQuantity),
        }),
      })

      if (response.status === 403) {
        showMessage("Access Denied: Admin only", "error")
        return
      }

      if (response.ok) {
        showMessage("Sweet added successfully!", "success")
        setShowAdminForm(null)
        setFormData({ ...formData, sweetName: "", sweetCategory: "", sweetPrice: "", sweetQuantity: "" })
        fetchSweets()
      } else {
        showMessage("Failed to add sweet", "error")
      }
    } catch (error) {
      showMessage("Failed to add sweet", "error")
    }
  }

  const handleUpdateSweet = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!selectedSweet) return

    const token = localStorage.getItem("access_token")
    try {
      const response = await fetch(`${API_BASE_URL}/api/sweets/${selectedSweet.id}/`, {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: formData.sweetName,
          category: formData.sweetCategory,
          price: Number.parseFloat(formData.sweetPrice),
          quantity: Number.parseInt(formData.sweetQuantity),
        }),
      })

      if (response.status === 403) {
        showMessage("Access Denied: Admin only", "error")
        return
      }

      if (response.ok) {
        showMessage("Sweet updated successfully!", "success")
        setShowAdminForm(null)
        setSelectedSweet(null)
        setFormData({ ...formData, sweetName: "", sweetCategory: "", sweetPrice: "", sweetQuantity: "" })
        fetchSweets()
      } else {
        showMessage("Failed to update sweet", "error")
      }
    } catch (error) {
      showMessage("Failed to update sweet", "error")
    }
  }

  const handleDeleteSweet = async (sweetId: number) => {
    if (!confirm("Are you sure you want to delete this sweet?")) return

    const token = localStorage.getItem("access_token")
    try {
      const response = await fetch(`${API_BASE_URL}/api/sweets/${sweetId}/`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      if (response.status === 403) {
        showMessage("Access Denied: Admin only", "error")
        return
      }

      if (response.ok) {
        showMessage("Sweet deleted successfully!", "success")
        fetchSweets()
      } else {
        showMessage("Failed to delete sweet", "error")
      }
    } catch (error) {
      showMessage("Failed to delete sweet", "error")
    }
  }

  const handleRestock = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!selectedSweet) return

    const token = localStorage.getItem("access_token")
    try {
      const response = await fetch(`${API_BASE_URL}/api/sweets/${selectedSweet.id}/restock/`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          quantity: Number.parseInt(formData.sweetQuantity),
        }),
      })

      if (response.status === 403) {
        showMessage("Access Denied: Admin only", "error")
        return
      }

      if (response.ok) {
        showMessage("Sweet restocked successfully!", "success")
        setShowAdminForm(null)
        setSelectedSweet(null)
        setFormData({ ...formData, sweetQuantity: "" })
        fetchSweets()
      } else {
        showMessage("Failed to restock sweet", "error")
      }
    } catch (error) {
      showMessage("Failed to restock sweet", "error")
    }
  }

  const openUpdateForm = (sweet: Sweet) => {
    setSelectedSweet(sweet)
    setFormData({
      ...formData,
      sweetName: sweet.name,
      sweetCategory: sweet.category,
      sweetPrice: sweet.price.toString(),
      sweetQuantity: sweet.quantity.toString(),
    })
    setShowAdminForm("update")
  }

  const openRestockForm = (sweet: Sweet) => {
    setSelectedSweet(sweet)
    setFormData({ ...formData, sweetQuantity: "" })
    setShowAdminForm("restock")
  }

  const categories = [...new Set(sweets.map((s) => s.category))]

  return (
    <div className="app-container">
      {/* Navbar */}
      <nav className="navbar">
        <div className="nav-content">
          <h1 className="logo">🍬 Sweet Shop</h1>
          <div className="nav-links">
            {isAuthenticated ? (
              <>
                <span className="user-info">Welcome, {user?.username}</span>
                {user?.is_staff && <span className="admin-badge">Admin</span>}
                <button onClick={handleLogout} className="btn-secondary">
                  Logout
                </button>
              </>
            ) : (
              <>
                <button onClick={() => setCurrentView("login")} className="btn-link">
                  Login
                </button>
                <button onClick={() => setCurrentView("register")} className="btn-primary">
                  Register
                </button>
              </>
            )}
          </div>
        </div>
      </nav>

      {/* Message Banner */}
      {message.text && <div className={`message-banner ${message.type}`}>{message.text}</div>}

      {/* Main Content */}
      <main className="main-content">
        {currentView === "login" && !isAuthenticated && (
          <div className="auth-container">
            <div className="auth-card">
              <h2>Login to Sweet Shop</h2>
              <form onSubmit={handleLogin}>
                <div className="form-group">
                  <label>Username</label>
                  <input
                    type="text"
                    value={formData.username}
                    onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Password</label>
                  <input
                    type="password"
                    value={formData.password}
                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                    required
                  />
                </div>
                <button type="submit" className="btn-primary btn-full">
                  Login
                </button>
              </form>
              <p className="auth-switch">
                Don't have an account?{" "}
                <button onClick={() => setCurrentView("register")} className="btn-link">
                  Register here
                </button>
              </p>
            </div>
          </div>
        )}

        {currentView === "register" && !isAuthenticated && (
          <div className="auth-container">
            <div className="auth-card">
              <h2>Create Account</h2>
              <form onSubmit={handleRegister}>
                <div className="form-group">
                  <label>Username</label>
                  <input
                    type="text"
                    value={formData.username}
                    onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Email</label>
                  <input
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Password</label>
                  <input
                    type="password"
                    value={formData.password}
                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                    required
                  />
                </div>
                <button type="submit" className="btn-primary btn-full">
                  Register
                </button>
              </form>
              <p className="auth-switch">
                Already have an account?{" "}
                <button onClick={() => setCurrentView("login")} className="btn-link">
                  Login here
                </button>
              </p>
            </div>
          </div>
        )}

        {currentView === "dashboard" && isAuthenticated && (
          <div className="dashboard-container">
            {/* Admin Panel */}
            {user?.is_staff && (
              <div className="admin-panel">
                <h2>Admin Controls</h2>
                <div className="admin-actions">
                  <button onClick={() => setShowAdminForm("add")} className="btn-admin">
                    + Add Sweet
                  </button>
                </div>

                {/* Admin Forms */}
                {showAdminForm === "add" && (
                  <div className="admin-form">
                    <h3>Add New Sweet</h3>
                    <form onSubmit={handleAddSweet}>
                      <div className="form-row">
                        <div className="form-group">
                          <label>Name</label>
                          <input
                            type="text"
                            value={formData.sweetName}
                            onChange={(e) => setFormData({ ...formData, sweetName: e.target.value })}
                            required
                          />
                        </div>
                        <div className="form-group">
                          <label>Category</label>
                          <input
                            type="text"
                            value={formData.sweetCategory}
                            onChange={(e) => setFormData({ ...formData, sweetCategory: e.target.value })}
                            required
                          />
                        </div>
                      </div>
                      <div className="form-row">
                        <div className="form-group">
                          <label>Price ($)</label>
                          <input
                            type="number"
                            step="0.01"
                            value={formData.sweetPrice}
                            onChange={(e) => setFormData({ ...formData, sweetPrice: e.target.value })}
                            required
                          />
                        </div>
                        <div className="form-group">
                          <label>Quantity</label>
                          <input
                            type="number"
                            value={formData.sweetQuantity}
                            onChange={(e) => setFormData({ ...formData, sweetQuantity: e.target.value })}
                            required
                          />
                        </div>
                      </div>
                      <div className="form-actions">
                        <button type="submit" className="btn-primary">
                          Add Sweet
                        </button>
                        <button type="button" onClick={() => setShowAdminForm(null)} className="btn-secondary">
                          Cancel
                        </button>
                      </div>
                    </form>
                  </div>
                )}

                {showAdminForm === "update" && selectedSweet && (
                  <div className="admin-form">
                    <h3>Update Sweet</h3>
                    <form onSubmit={handleUpdateSweet}>
                      <div className="form-row">
                        <div className="form-group">
                          <label>Name</label>
                          <input
                            type="text"
                            value={formData.sweetName}
                            onChange={(e) => setFormData({ ...formData, sweetName: e.target.value })}
                            required
                          />
                        </div>
                        <div className="form-group">
                          <label>Category</label>
                          <input
                            type="text"
                            value={formData.sweetCategory}
                            onChange={(e) => setFormData({ ...formData, sweetCategory: e.target.value })}
                            required
                          />
                        </div>
                      </div>
                      <div className="form-row">
                        <div className="form-group">
                          <label>Price ($)</label>
                          <input
                            type="number"
                            step="0.01"
                            value={formData.sweetPrice}
                            onChange={(e) => setFormData({ ...formData, sweetPrice: e.target.value })}
                            required
                          />
                        </div>
                        <div className="form-group">
                          <label>Quantity</label>
                          <input
                            type="number"
                            value={formData.sweetQuantity}
                            onChange={(e) => setFormData({ ...formData, sweetQuantity: e.target.value })}
                            required
                          />
                        </div>
                      </div>
                      <div className="form-actions">
                        <button type="submit" className="btn-primary">
                          Update Sweet
                        </button>
                        <button
                          type="button"
                          onClick={() => {
                            setShowAdminForm(null)
                            setSelectedSweet(null)
                          }}
                          className="btn-secondary"
                        >
                          Cancel
                        </button>
                      </div>
                    </form>
                  </div>
                )}

                {showAdminForm === "restock" && selectedSweet && (
                  <div className="admin-form">
                    <h3>Restock: {selectedSweet.name}</h3>
                    <form onSubmit={handleRestock}>
                      <div className="form-group">
                        <label>Add Quantity</label>
                        <input
                          type="number"
                          value={formData.sweetQuantity}
                          onChange={(e) => setFormData({ ...formData, sweetQuantity: e.target.value })}
                          required
                          min="1"
                        />
                      </div>
                      <div className="form-actions">
                        <button type="submit" className="btn-primary">
                          Restock
                        </button>
                        <button
                          type="button"
                          onClick={() => {
                            setShowAdminForm(null)
                            setSelectedSweet(null)
                          }}
                          className="btn-secondary"
                        >
                          Cancel
                        </button>
                      </div>
                    </form>
                  </div>
                )}
              </div>
            )}

            {/* Search and Filter */}
            <div className="filter-section">
              <h2>Browse Our Sweets</h2>
              <div className="filters">
                <div className="filter-group">
                  <input
                    type="text"
                    placeholder="Search by name or category..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="search-input"
                  />
                </div>
                <div className="filter-row">
                  <select
                    value={categoryFilter}
                    onChange={(e) => setCategoryFilter(e.target.value)}
                    className="filter-select"
                  >
                    <option value="">All Categories</option>
                    {categories.map((cat) => (
                      <option key={cat} value={cat}>
                        {cat}
                      </option>
                    ))}
                  </select>
                  <input
                    type="number"
                    placeholder="Min Price"
                    value={minPrice}
                    onChange={(e) => setMinPrice(e.target.value)}
                    className="filter-input"
                  />
                  <input
                    type="number"
                    placeholder="Max Price"
                    value={maxPrice}
                    onChange={(e) => setMaxPrice(e.target.value)}
                    className="filter-input"
                  />
                  {(searchTerm || categoryFilter || minPrice || maxPrice) && (
                    <button
                      onClick={() => {
                        setSearchTerm("")
                        setCategoryFilter("")
                        setMinPrice("")
                        setMaxPrice("")
                      }}
                      className="btn-clear"
                    >
                      Clear Filters
                    </button>
                  )}
                </div>
              </div>
            </div>

            {/* Sweets Grid */}
            <div className="sweets-grid">
              {filteredSweets.length === 0 ? (
                <div className="empty-state">
                  <p>No sweets found. Try adjusting your filters!</p>
                </div>
              ) : (
                filteredSweets.map((sweet) => (
                  <div key={sweet.id} className="sweet-card">
                    <div className="sweet-header">
                      <h3>{sweet.name}</h3>
                      <span className="category-badge">{sweet.category}</span>
                    </div>
                    <div className="sweet-details">
                      <div className="price">${sweet.price.toFixed(2)}</div>
                      <div className={`quantity ${sweet.quantity === 0 ? "out-of-stock" : ""}`}>
                        {sweet.quantity > 0 ? `${sweet.quantity} in stock` : "Out of stock"}
                      </div>
                    </div>
                    <div className="sweet-actions">
                      <button
                        onClick={() => handlePurchase(sweet.id)}
                        disabled={sweet.quantity === 0}
                        className="btn-purchase"
                      >
                        {sweet.quantity === 0 ? "Out of Stock" : "Purchase"}
                      </button>
                      {user?.is_staff && (
                        <div className="admin-buttons">
                          <button onClick={() => openUpdateForm(sweet)} className="btn-icon" title="Edit">
                            ✏️
                          </button>
                          <button onClick={() => openRestockForm(sweet)} className="btn-icon" title="Restock">
                            📦
                          </button>
                          <button
                            onClick={() => handleDeleteSweet(sweet.id)}
                            className="btn-icon btn-delete"
                            title="Delete"
                          >
                            🗑️
                          </button>
                        </div>
                      )}
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
