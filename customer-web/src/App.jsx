import { useAuth0 } from '@auth0/auth0-react'
import { useEffect, useState } from 'react'
import { BrowserRouter, Link, NavLink, Route, Routes, useParams, useSearchParams } from 'react-router-dom'

const products = [
  {
    id: 'p-1',
    name: 'Aurora Lamp',
    price: 89,
    category: 'Home',
    stock: 12,
    image: 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=900&q=80',
    description: 'Warm ambient lighting with a modern silhouette for cozy rooms.',
    popularity: 96,
  },
  {
    id: 'p-2',
    name: 'Peak Backpack',
    price: 124,
    category: 'Travel',
    stock: 7,
    image: 'https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?auto=format&fit=crop&w=900&q=80',
    description: 'A smart, weather-ready backpack built for everyday movement.',
    popularity: 91,
  },
  {
    id: 'p-3',
    name: 'Luma Watch',
    price: 159,
    category: 'Electronics',
    stock: 4,
    image: 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=900&q=80',
    description: 'Minimal design, precise tracking, and reliable battery life.',
    popularity: 94,
  },
  {
    id: 'p-4',
    name: 'Cedar Chair',
    price: 210,
    category: 'Furniture',
    stock: 3,
    image: 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=900&q=80',
    description: 'An ergonomic accent chair for modern workspaces and reading corners.',
    popularity: 88,
  },
]

const categories = [...new Set(products.map((product) => product.category))]
const auth0Configured = Boolean(import.meta.env.VITE_AUTH0_DOMAIN && import.meta.env.VITE_AUTH0_CLIENT_ID)
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const orders = [
  { id: 'ORD-1001', total: 142.0, status: 'Confirmed', date: '2026-10-01' },
  { id: 'ORD-1002', total: 89.0, status: 'Shipped', date: '2026-09-28' },
]

const notifications = [
  { id: 1, text: 'Payment succeeded for ORD-1001', unread: true },
  { id: 2, text: 'Your order has been shipped', unread: false },
  { id: 3, text: 'Low stock alert: Aurora Lamp', unread: true },
]

const adminStats = [
  { label: 'Total sales', value: '$42.8K' },
  { label: 'Total orders', value: '1,245' },
  { label: 'Successful payments', value: '97.4%' },
  { label: 'Low stock', value: '17 items' },
]

const navItems = [
  { label: 'Home', path: '/' },
  { label: 'Products', path: '/products' },
  { label: 'Cart', path: '/cart' },
  { label: 'Orders', path: '/orders' },
  { label: 'Notifications', path: '/notifications' },
  { label: 'Admin', path: '/admin' },
]

function AppShell() {
  return (
    <div className="min-h-screen bg-slate-100 text-slate-900">
      {auth0Configured && <ProfileSync />}
      <header className="border-b border-slate-200 bg-white/90 backdrop-blur-sm">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4">
          <Link to="/" className="text-2xl font-black tracking-tight text-slate-900">
            NEXA<span className="text-amber-500">SHOP</span>
          </Link>
          <nav className="hidden gap-6 md:flex">
            {navItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `font-medium transition ${isActive ? 'text-amber-600' : 'text-slate-600 hover:text-slate-900'}`
                }
              >
                {item.label}
              </NavLink>
            ))}
          </nav>
          <div className="flex items-center gap-3">
            <Link to="/login" className="rounded-full border border-slate-300 px-4 py-2 text-sm font-semibold hover:bg-slate-50">
              Login
            </Link>
            <Link to="/register" className="rounded-full bg-amber-400 px-4 py-2 text-sm font-semibold text-slate-900 hover:bg-amber-300">
              Sign up
            </Link>
            <Link to="/checkout" className="rounded-full bg-slate-900 px-4 py-2 text-sm font-semibold text-white hover:bg-slate-700">
              Checkout
            </Link>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 py-8">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/products" element={<ProductsPage />} />
          <Route path="/products/:id" element={<ProductDetailPage />} />
          <Route path="/login" element={<AuthPage mode="login" />} />
          <Route path="/register" element={<AuthPage mode="register" />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/cart" element={<CartPage />} />
          <Route path="/checkout" element={<CheckoutPage />} />
          <Route path="/orders" element={<OrdersPage />} />
          <Route path="/orders/:id" element={<OrderDetailPage />} />
          <Route path="/notifications" element={<NotificationsPage />} />
          <Route path="/profile" element={<ProfilePage />} />
          <Route path="/admin" element={<AdminPage />} />
        </Routes>
      </main>
    </div>
  )
}

function HomePage() {
  return (
    <div className="space-y-10">
      <section className="overflow-hidden rounded-3xl bg-gradient-to-r from-slate-900 via-slate-800 to-slate-700 text-white shadow-xl">
        <div className="grid gap-8 p-8 md:grid-cols-2 md:p-12">
          <div className="space-y-6">
            <span className="inline-flex rounded-full bg-white/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-slate-200">
              New season arrivals
            </span>
            <h1 className="text-4xl font-black tracking-tight md:text-6xl">
              Shop smarter. Live better.
            </h1>
            <p className="max-w-lg text-lg text-slate-300">
              Discover premium essentials, fast checkout, and a seamless customer journey built for modern commerce.
            </p>
            <div className="flex gap-4">
              <Link to="/products" className="rounded-full bg-amber-400 px-6 py-3 font-semibold text-slate-900 hover:bg-amber-300">
                Browse products
              </Link>
              <Link to="/register" className="rounded-full border border-white/20 px-6 py-3 font-semibold text-white hover:bg-white/5">
                Join now
              </Link>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            {products.slice(0, 4).map((product) => (
              <div key={product.id} className="rounded-2xl bg-white/5 p-3 backdrop-blur-sm">
                <img src={product.image} alt={product.name} className="h-32 w-full rounded-xl object-cover" />
                <p className="mt-3 font-semibold">{product.name}</p>
                <p className="text-sm text-slate-300">${product.price}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="space-y-5">
        <div className="flex items-end justify-between">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.2em] text-slate-500">Browse by category</p>
            <h2 className="mt-1 text-3xl font-black">Find your next favorite</h2>
          </div>
          <Link to="/products" className="font-semibold text-amber-700 hover:text-amber-800">View all products →</Link>
        </div>
        <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
          {categories.map((category) => {
            const count = products.filter((product) => product.category === category).length
            return (
              <Link
                key={category}
                to={`/products?category=${encodeURIComponent(category)}`}
                className="rounded-2xl bg-white p-5 shadow-sm ring-1 ring-slate-200 transition hover:-translate-y-1 hover:shadow-md"
              >
                <span className="text-lg font-bold">{category}</span>
                <span className="mt-1 block text-sm text-slate-500">{count} {count === 1 ? 'product' : 'products'}</span>
              </Link>
            )
          })}
        </div>
      </section>

      <section className="space-y-5">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-slate-500">The collection</p>
          <h2 className="mt-1 text-3xl font-black">Shop all products</h2>
        </div>
        <ProductGrid items={products} />
      </section>

      <section className="grid gap-6 md:grid-cols-3">
        {[
          { title: 'Fast checkout', text: 'Secure Stripe checkout and clear payment status updates.' },
          { title: 'Realtime updates', text: 'Order and stock notifications instantly pushed to customers.' },
          { title: 'Admin analytics', text: 'Track revenue, product demand, and low-stock alerts.' },
        ].map((item) => (
          <div key={item.title} className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
            <h2 className="mb-2 text-xl font-bold">{item.title}</h2>
            <p className="text-slate-600">{item.text}</p>
          </div>
        ))}
      </section>
    </div>
  )
}

function ProductsPage() {
  const [searchParams, setSearchParams] = useSearchParams()
  const [search, setSearch] = useState('')
  const [sort, setSort] = useState('popular')
  const selectedCategory = searchParams.get('category') || 'All'
  const visibleProducts = products
    .filter((product) => selectedCategory === 'All' || product.category === selectedCategory)
    .filter((product) => `${product.name} ${product.description}`.toLowerCase().includes(search.toLowerCase()))
    .sort((first, second) => {
      if (sort === 'price-low') return first.price - second.price
      if (sort === 'price-high') return second.price - first.price
      return second.popularity - first.popularity
    })

  function selectCategory(category) {
    setSearchParams(category === 'All' ? {} : { category })
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-slate-500">Catalog</p>
          <h1 className="mt-1 text-3xl font-black">Shop all products</h1>
        </div>
        <span className="rounded-full bg-white px-4 py-2 text-sm shadow-sm ring-1 ring-slate-200">
          {visibleProducts.length} {visibleProducts.length === 1 ? 'item' : 'items'}
        </span>
      </div>

      <div className="flex flex-col gap-4 rounded-2xl bg-white p-4 shadow-sm ring-1 ring-slate-200 md:flex-row">
        <label className="flex-1">
          <span className="sr-only">Search products</span>
          <input
            type="search"
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            placeholder="Search products..."
            className="w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-amber-500"
          />
        </label>
        <label>
          <span className="sr-only">Sort products</span>
          <select value={sort} onChange={(event) => setSort(event.target.value)} className="w-full rounded-xl border border-slate-300 bg-white px-4 py-3 md:w-auto">
            <option value="popular">Most popular</option>
            <option value="price-low">Price: low to high</option>
            <option value="price-high">Price: high to low</option>
          </select>
        </label>
      </div>

      <div className="flex flex-wrap gap-2">
        {['All', ...categories].map((category) => (
          <button
            key={category}
            type="button"
            onClick={() => selectCategory(category)}
            aria-pressed={selectedCategory === category}
            className={`rounded-full px-4 py-2 text-sm font-semibold transition ${
              selectedCategory === category
                ? 'bg-slate-900 text-white'
                : 'bg-white text-slate-700 ring-1 ring-slate-200 hover:bg-slate-50'
            }`}
          >
            {category}
          </button>
        ))}
      </div>

      {visibleProducts.length ? (
        <ProductGrid items={visibleProducts} />
      ) : (
        <p className="rounded-2xl bg-white p-8 text-center text-slate-600 ring-1 ring-slate-200">
          No products match your search. Try another name or category.
        </p>
      )}
    </div>
  )
}

function ProductGrid({ items }) {
  return (
    <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
      {items.map((product) => (
          <div key={product.id} className="overflow-hidden rounded-3xl bg-white shadow-sm ring-1 ring-slate-200">
            <img src={product.image} alt={product.name} className="h-56 w-full object-cover" />
            <div className="space-y-4 p-5">
              <div className="flex items-center justify-between">
                <span className="rounded-full bg-amber-100 px-2 py-1 text-xs font-semibold text-amber-700">{product.category}</span>
                <span className="text-sm text-slate-500">{product.stock} in stock</span>
              </div>
              <div>
                <h2 className="text-xl font-bold">{product.name}</h2>
                <p className="mt-2 text-sm text-slate-600">{product.description}</p>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-2xl font-black">${product.price}</span>
                <Link to={`/products/${product.id}`} className="rounded-full bg-slate-900 px-4 py-2 text-sm font-semibold text-white hover:bg-slate-700">
                  View item
                </Link>
              </div>
            </div>
          </div>
      ))}
    </div>
  )
}

function ProductDetailPage() {
  const { id } = useParams()
  const product = products.find((item) => item.id === id) || products[0]

  return (
    <div className="grid gap-8 md:grid-cols-2">
      <div className="overflow-hidden rounded-3xl bg-white p-3 shadow-sm ring-1 ring-slate-200">
        <img src={product.image} alt={product.name} className="h-[420px] w-full rounded-2xl object-cover" />
      </div>
      <div className="space-y-6 rounded-3xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-slate-500">{product.category}</p>
          <h1 className="mt-2 text-4xl font-black">{product.name}</h1>
        </div>
        <p className="text-slate-600">{product.description}</p>
        <div className="flex items-center gap-6">
          <span className="text-4xl font-black text-slate-900">${product.price}</span>
          <span className="rounded-full bg-green-100 px-3 py-1 text-sm font-semibold text-green-700">{product.stock} left</span>
        </div>
        <div className="flex gap-3">
          <button className="rounded-full bg-slate-900 px-5 py-3 font-semibold text-white hover:bg-slate-700">
            Add to cart
          </button>
          <Link to="/checkout" className="rounded-full border border-slate-300 px-5 py-3 font-semibold hover:bg-slate-50">
            Buy now
          </Link>
        </div>
      </div>
    </div>
  )
}

function AuthPage({ mode }) {
  if (!auth0Configured) {
    return <AuthSetupNotice mode={mode} />
  }

  return <ConfiguredAuthPage mode={mode} />
}

function ProfileSync() {
  const { isAuthenticated, getAccessTokenSilently } = useAuth0()
  const [status, setStatus] = useState('')

  useEffect(() => {
    let cancelled = false

    if (!isAuthenticated) {
      return () => {
        cancelled = true
      }
    }

    async function syncProfile() {
      try {
        const token = await getAccessTokenSilently()
        const response = await fetch(`${apiBaseUrl}/api/users/me`, {
          headers: { Authorization: `Bearer ${token}` },
        })
        if (!response.ok) throw new Error(`API returned ${response.status}`)
        await response.json()
        if (!cancelled) setStatus('Your customer profile is synced.')
      } catch (error) {
        if (!cancelled) {
          setStatus(`Profile sync failed: ${error instanceof Error ? error.message : 'Unknown error'}`)
        }
      }
    }

    void syncProfile()
    return () => {
      cancelled = true
    }
  }, [getAccessTokenSilently, isAuthenticated])

  if (!isAuthenticated || !status) return null

  return (
    <p role="status" className="bg-slate-900 px-4 py-2 text-center text-sm text-white">
      {status}
    </p>
  )
}

function AuthSetupNotice({ mode }) {
  return (
    <div className="mx-auto max-w-md rounded-3xl bg-white p-8 shadow-sm ring-1 ring-slate-200">
      <h1 className="mb-6 text-3xl font-black">{mode === 'login' ? 'Welcome back' : 'Create account'}</h1>
      <p className="rounded-xl bg-amber-50 p-4 text-sm text-amber-900">
        Sign-in is not configured yet. Add your Auth0 domain and client ID to
        <code className="mx-1">customer-web/.env</code> to enable secure account access.
      </p>
      <AuthModeSwitch mode={mode} />
    </div>
  )
}

function ConfiguredAuthPage({ mode }) {
  const { loginWithRedirect, isLoading, error } = useAuth0()
  const isRegister = mode === 'register'

  const startAuth = () =>
    loginWithRedirect({
      authorizationParams: isRegister ? { screen_hint: 'signup' } : {},
    })

  return (
    <div className="mx-auto max-w-md rounded-3xl bg-white p-8 shadow-sm ring-1 ring-slate-200">
      <h1 className="text-3xl font-black">{isRegister ? 'Create your account' : 'Welcome back'}</h1>
      <p className="mt-2 text-slate-600">
        {isRegister ? 'Sign up securely with your email or a connected social account.' : 'Sign in to continue to your account.'}
      </p>
      {error && <p role="alert" className="mt-5 rounded-xl bg-red-50 p-3 text-sm text-red-700">{error.message}</p>}
      <button
        type="button"
        onClick={startAuth}
        disabled={isLoading}
        className="mt-6 w-full rounded-xl bg-slate-900 px-4 py-3 font-semibold text-white hover:bg-slate-700 disabled:cursor-not-allowed disabled:opacity-60"
      >
        {isLoading ? 'Please wait…' : isRegister ? 'Continue to sign up' : 'Continue to sign in'}
      </button>
      <p className="mt-4 text-center text-xs text-slate-500">
        Email/password and any enabled Google or Facebook options are managed securely by Auth0.
      </p>
      <AuthModeSwitch mode={mode} />
    </div>
  )
}

function AuthModeSwitch({ mode }) {
  const isRegister = mode === 'register'

  return (
    <p className="mt-6 text-center text-sm text-slate-600">
      {isRegister ? 'Already have an account?' : "Don't have an account?"}{' '}
      <Link to={isRegister ? '/login' : '/register'} className="font-semibold text-amber-700 underline underline-offset-2">
        {isRegister ? 'Sign in' : 'Sign up'}
      </Link>
    </p>
  )
}

function DashboardPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-black">Dashboard</h1>
      <div className="grid gap-4 md:grid-cols-4">
        {adminStats.map((stat) => (
          <div key={stat.label} className="rounded-2xl bg-white p-5 shadow-sm ring-1 ring-slate-200">
            <p className="text-sm text-slate-500">{stat.label}</p>
            <p className="mt-3 text-2xl font-black">{stat.value}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

function CartPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-black">Shopping cart</h1>
      <div className="grid gap-6 lg:grid-cols-[2fr_1fr]">
        <div className="space-y-4">
          {products.slice(0, 2).map((product) => (
            <div key={product.id} className="flex items-center justify-between rounded-2xl bg-white p-4 shadow-sm ring-1 ring-slate-200">
              <div className="flex items-center gap-4">
                <img src={product.image} alt={product.name} className="h-20 w-20 rounded-xl object-cover" />
                <div>
                  <p className="font-bold">{product.name}</p>
                  <p className="text-sm text-slate-500">Qty: 1</p>
                </div>
              </div>
              <p className="font-bold">${product.price}</p>
            </div>
          ))}
        </div>
        <div className="rounded-3xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
          <h2 className="text-xl font-bold">Summary</h2>
          <div className="mt-6 space-y-3 text-slate-600">
            <div className="flex justify-between"><span>Subtotal</span><span>$213</span></div>
            <div className="flex justify-between"><span>Shipping</span><span>$12</span></div>
            <div className="flex justify-between border-t border-slate-200 pt-3 text-lg font-bold text-slate-900"><span>Total</span><span>$225</span></div>
          </div>
          <Link to="/checkout" className="mt-6 block rounded-xl bg-slate-900 px-4 py-3 text-center font-semibold text-white hover:bg-slate-700">
            Proceed to checkout
          </Link>
        </div>
      </div>
    </div>
  )
}

function CheckoutPage() {
  return (
    <div className="mx-auto max-w-3xl rounded-3xl bg-white p-8 shadow-sm ring-1 ring-slate-200">
      <h1 className="text-3xl font-black">Checkout</h1>
      <div className="mt-6 grid gap-6 md:grid-cols-2">
        <div className="space-y-4">
          <div>
            <label className="mb-1 block text-sm font-medium">Cardholder name</label>
            <input className="w-full rounded-xl border border-slate-300 px-3 py-2" defaultValue="Jane Doe" />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium">Email</label>
            <input className="w-full rounded-xl border border-slate-300 px-3 py-2" defaultValue="jane@example.com" />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium">Stripe test card</label>
            <input className="w-full rounded-xl border border-slate-300 px-3 py-2" defaultValue="4242 4242 4242 4242" />
          </div>
        </div>
        <div className="rounded-2xl bg-slate-50 p-5">
          <h2 className="text-xl font-bold">Order summary</h2>
          <div className="mt-4 space-y-3 text-slate-600">
            <div className="flex justify-between"><span>Aurora Lamp</span><span>$89</span></div>
            <div className="flex justify-between"><span>Peak Backpack</span><span>$124</span></div>
            <div className="flex justify-between border-t border-slate-300 pt-3 text-lg font-bold text-slate-900"><span>Total</span><span>$213</span></div>
          </div>
        </div>
      </div>
      <button className="mt-8 w-full rounded-xl bg-amber-500 px-4 py-3 font-semibold text-slate-900 hover:bg-amber-400">
        Pay securely with Stripe
      </button>
    </div>
  )
}

function OrdersPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-black">Orders</h1>
      <div className="space-y-4">
        {orders.map((order) => (
          <div key={order.id} className="flex items-center justify-between rounded-2xl bg-white p-5 shadow-sm ring-1 ring-slate-200">
            <div>
              <p className="text-lg font-bold">{order.id}</p>
              <p className="text-sm text-slate-500">{order.date}</p>
            </div>
            <div className="flex items-center gap-4">
              <span className="rounded-full bg-emerald-100 px-3 py-1 text-sm font-semibold text-emerald-700">{order.status}</span>
              <span className="text-lg font-bold">${order.total}</span>
              <Link to={`/orders/${order.id}`} className="rounded-full border border-slate-300 px-4 py-2 text-sm font-semibold hover:bg-slate-50">
                Details
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

function OrderDetailPage() {
  return (
    <div className="rounded-3xl bg-white p-8 shadow-sm ring-1 ring-slate-200">
      <h1 className="text-3xl font-black">Order details</h1>
      <div className="mt-6 grid gap-8 md:grid-cols-2">
        <div>
          <p className="text-sm uppercase tracking-[0.2em] text-slate-500">Order ID</p>
          <p className="mt-2 text-2xl font-bold">ORD-1001</p>
          <p className="mt-6 text-slate-600">Status: Confirmed</p>
          <p className="text-slate-600">Payment status: Paid</p>
        </div>
        <div className="rounded-2xl bg-slate-50 p-5">
          <div className="flex justify-between"><span>Aurora Lamp</span><span>$89</span></div>
          <div className="mt-3 flex justify-between"><span>Peak Backpack</span><span>$124</span></div>
          <div className="mt-5 flex justify-between border-t border-slate-200 pt-3 text-lg font-bold"><span>Total</span><span>$213</span></div>
        </div>
      </div>
    </div>
  )
}

function NotificationsPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-black">Notifications</h1>
      <div className="space-y-4">
        {notifications.map((notification) => (
          <div key={notification.id} className={`rounded-2xl p-4 shadow-sm ring-1 ${notification.unread ? 'bg-amber-50 ring-amber-200' : 'bg-white ring-slate-200'}`}>
            <div className="flex items-center justify-between gap-4">
              <p className="font-medium">{notification.text}</p>
              {notification.unread && <span className="rounded-full bg-amber-500 px-2 py-1 text-xs font-bold text-white">New</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

function ProfilePage() {
  return (
    <div className="mx-auto max-w-2xl rounded-3xl bg-white p-8 shadow-sm ring-1 ring-slate-200">
      <h1 className="text-3xl font-black">Profile</h1>
      <div className="mt-6 space-y-4">
        <div>
          <label className="mb-1 block text-sm font-medium">Name</label>
          <input className="w-full rounded-xl border border-slate-300 px-3 py-2" defaultValue="Jane Doe" />
        </div>
        <div>
          <label className="mb-1 block text-sm font-medium">Email</label>
          <input className="w-full rounded-xl border border-slate-300 px-3 py-2" defaultValue="jane@example.com" />
        </div>
        <button className="w-full rounded-xl bg-slate-900 px-4 py-3 font-semibold text-white hover:bg-slate-700">
          Save profile
        </button>
      </div>
    </div>
  )
}

function AdminPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-black">Admin dashboard</h1>
      <div className="grid gap-4 md:grid-cols-4">
        {adminStats.map((stat) => (
          <div key={stat.label} className="rounded-2xl bg-slate-900 p-5 text-white shadow-sm">
            <p className="text-sm text-slate-300">{stat.label}</p>
            <p className="mt-3 text-2xl font-black">{stat.value}</p>
          </div>
        ))}
      </div>
      <div className="grid gap-6 md:grid-cols-2">
        <div className="rounded-3xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
          <h2 className="text-xl font-bold">Recent orders</h2>
          <div className="mt-4 space-y-3">
            {orders.map((order) => (
              <div key={order.id} className="flex items-center justify-between border-b border-slate-200 pb-2 last:border-none">
                <span>{order.id}</span>
                <span>{order.status}</span>
              </div>
            ))}
          </div>
        </div>
        <div className="rounded-3xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
          <h2 className="text-xl font-bold">Popular items</h2>
          <div className="mt-4 space-y-3">
            {products.map((product) => (
              <div key={product.id} className="flex items-center justify-between">
                <span>{product.name}</span>
                <span>{product.popularity}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <AppShell />
    </BrowserRouter>
  )
}
