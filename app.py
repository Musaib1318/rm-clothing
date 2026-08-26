from flask import Flask, render_template_string, session, redirect, url_for, request

app = Flask(__name__)
app.secret_key = "rm_clothing_secret_key_2026"

# ==================== PRODUCTS (Budget to Luxury) ====================
products = {
    # ===== MEN - Budget =====
    1: {"name": "Basic Cotton T-Shirt", "price": 399, "category": "Men", "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=600", "desc": "Soft cotton everyday t-shirt. Comfortable and affordable."},
    2: {"name": "Regular Fit Jeans", "price": 899, "category": "Men", "image": "https://images.unsplash.com/photo-1542272454315-4c01d7abdf4a?w=600", "desc": "Classic blue jeans for daily wear."},
    3: {"name": "Casual Shirt", "price": 699, "category": "Men", "image": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=600", "desc": "Lightweight casual shirt for office or outing."},
    4: {"name": "Sports Shorts", "price": 499, "category": "Men", "image": "https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=600", "desc": "Breathable sports shorts for gym and running."},

    # ===== MEN - Mid Range =====
    5: {"name": "Oxford Formal Shirt", "price": 1499, "category": "Men", "image": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=600", "desc": "Premium cotton Oxford shirt for formal occasions."},
    6: {"name": "Slim Fit Chinos", "price": 1799, "category": "Men", "image": "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=600", "desc": "Modern slim-fit chinos with stretch fabric."},
    7: {"name": "Hooded Sweatshirt", "price": 1599, "category": "Men", "image": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=600", "desc": "Warm and stylish hoodie for winter."},
    8: {"name": "Denim Jacket", "price": 2499, "category": "Men", "image": "https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=600", "desc": "Classic denim jacket for casual looks."},

    # ===== MEN - Premium / Luxury =====
    9: {"name": "Leather Biker Jacket", "price": 8999, "category": "Men", "image": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=600", "desc": "Genuine leather biker jacket with premium finish."},
    10: {"name": "Cashmere Sweater", "price": 7499, "category": "Men", "image": "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=600", "desc": "Soft pure cashmere sweater for luxury comfort."},
    11: {"name": "Designer Blazer", "price": 9999, "category": "Men", "image": "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=600", "desc": "Elegant tailored blazer for formal events."},
    12: {"name": "Italian Wool Suit", "price": 18999, "category": "Men", "image": "https://images.unsplash.com/photo-1598808503746-f34afa71d6f9?w=600", "desc": "Premium Italian wool formal suit."},

    # ===== WOMEN - Budget =====
    13: {"name": "Basic Crop Top", "price": 449, "category": "Women", "image": "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=600", "desc": "Comfortable cotton crop top."},
    14: {"name": "High-Waist Jeans", "price": 999, "category": "Women", "image": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=600", "desc": "Stretchable high-waist jeans."},
    15: {"name": "Floral Kurti", "price": 799, "category": "Women", "image": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=600", "desc": "Light and pretty floral kurti."},
    16: {"name": "Cotton Palazzo", "price": 699, "category": "Women", "image": "https://images.unsplash.com/photo-1585487000160-6ebcfceb0d03?w=600", "desc": "Comfortable wide-leg cotton palazzo."},

    # ===== WOMEN - Mid Range =====
    17: {"name": "Summer Maxi Dress", "price": 1899, "category": "Women", "image": "https://images.unsplash.com/photo-1572804013305-25c0f0b2b0b0?w=600", "desc": "Flowy maxi dress perfect for summer."},
    18: {"name": "Knit Cardigan", "price": 1699, "category": "Women", "image": "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=600", "desc": "Soft knit cardigan for layering."},
    19: {"name": "Formal Trousers", "price": 1599, "category": "Women", "image": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=600", "desc": "Office-ready formal trousers."},
    20: {"name": "Embroidered Top", "price": 1299, "category": "Women", "image": "https://images.unsplash.com/photo-1564257631407-4deb1f99d992?w=600", "desc": "Beautiful embroidered ethnic top."},

    # ===== WOMEN - Premium / Luxury =====
    21: {"name": "Silk Evening Gown", "price": 12999, "category": "Women", "image": "https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=600", "desc": "Elegant silk gown for parties and events."},
    22: {"name": "Designer Saree", "price": 8999, "category": "Women", "image": "https://images.unsplash.com/photo-1610030469983-98e550d6183e?w=600", "desc": "Premium designer silk saree."},
    23: {"name": "Cashmere Shawl", "price": 6999, "category": "Women", "image": "https://images.unsplash.com/photo-1601924994987-69e26d50dc26?w=600", "desc": "Luxurious pure cashmere shawl."},
    24: {"name": "Leather Handbag", "price": 7999, "category": "Women", "image": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=600", "desc": "Genuine leather luxury handbag."},

    # ===== KIDS =====
    25: {"name": "Kids Graphic T-Shirt", "price": 399, "category": "Kids", "image": "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=600", "desc": "Fun printed t-shirt for kids."},
    26: {"name": "Kids Denim Jeans", "price": 699, "category": "Kids", "image": "https://images.unsplash.com/photo-1503919545889-aef636e10ad4?w=600", "desc": "Durable denim jeans for children."},
    27: {"name": "Kids Hoodie", "price": 899, "category": "Kids", "image": "https://images.unsplash.com/photo-1503919545889-aef636e10ad4?w=600", "desc": "Warm and soft hoodie for kids."},
    28: {"name": "Party Frock", "price": 1299, "category": "Kids", "image": "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=600", "desc": "Cute party frock for little girls."},

    # ===== ACCESSORIES =====
    29: {"name": "Cotton Cap", "price": 299, "category": "Accessories", "image": "https://images.unsplash.com/photo-1588850561407-ed78c314e07f?w=600", "desc": "Simple and stylish cotton cap."},
    30: {"name": "Leather Belt", "price": 799, "category": "Accessories", "image": "https://images.unsplash.com/photo-1624222247344-550fb605f483?w=600", "desc": "Classic genuine leather belt."},
    31: {"name": "Wool Scarf", "price": 999, "category": "Accessories", "image": "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=600", "desc": "Warm wool scarf for winter."},
    32: {"name": "Sunglasses", "price": 1499, "category": "Accessories", "image": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=600", "desc": "UV protection stylish sunglasses."},
    33: {"name": "Premium Watch", "price": 4999, "category": "Accessories", "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600", "desc": "Elegant analog premium watch."},
    34: {"name": "Designer Wallet", "price": 2499, "category": "Accessories", "image": "https://images.unsplash.com/photo-1627123424574-724758594e93?w=600", "desc": "Premium leather wallet."},
}

# ==================== BASE STYLE ====================
BASE_STYLE = """
<style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
        font-family: 'Segoe UI', system-ui, sans-serif;
        background: #f7f3ef;
        color: #1a1a1a;
        line-height: 1.6;
    }
    header {
        background: #111;
        color: white;
        padding: 16px 40px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: sticky;
        top: 0;
        z-index: 100;
        box-shadow: 0 2px 12px rgba(0,0,0,0.2);
    }
    .logo {
        font-size: 26px;
        font-weight: 700;
        letter-spacing: 3px;
    }
    .logo span { color: #d4a84b; }
    nav a {
        color: #eee;
        text-decoration: none;
        margin-left: 28px;
        font-weight: 500;
        font-size: 15px;
        transition: 0.25s;
    }
    nav a:hover { color: #d4a84b; }
    .cart-count {
        background: #d4a84b;
        color: #111;
        font-size: 12px;
        padding: 2px 7px;
        border-radius: 50px;
        margin-left: 4px;
    }
    .hero {
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)),
                    url('https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=1600') center/cover;
        height: 420px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        color: white;
    }
    .hero h1 { font-size: 46px; margin-bottom: 12px; letter-spacing: 1px; }
    .hero p { font-size: 18px; margin-bottom: 28px; opacity: 0.9; }
    .btn {
        display: inline-block;
        padding: 13px 32px;
        background: #d4a84b;
        color: #111;
        text-decoration: none;
        font-weight: 600;
        border-radius: 6px;
        border: none;
        cursor: pointer;
        transition: 0.25s;
        font-size: 15px;
    }
    .btn:hover { background: #c0953a; transform: translateY(-2px); }
    .btn-outline {
        background: transparent;
        border: 2px solid #d4a84b;
        color: #d4a84b;
    }
    .btn-outline:hover { background: #d4a84b; color: #111; }
    .section {
        max-width: 1200px;
        margin: 50px auto;
        padding: 0 20px;
    }
    .section h2 {
        text-align: center;
        font-size: 30px;
        margin-bottom: 35px;
    }
    .section h2::after {
        content: '';
        display: block;
        width: 55px;
        height: 3px;
        background: #d4a84b;
        margin: 10px auto 0;
    }
    .products {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 28px;
    }
    .product-card {
        background: white;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 14px rgba(0,0,0,0.07);
        transition: 0.3s;
        text-decoration: none;
        color: inherit;
        display: block;
    }
    .product-card:hover {
        transform: translateY(-7px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.12);
    }
    .product-img {
        height: 260px;
        background-size: cover;
        background-position: center;
    }
    .product-info { padding: 18px; }
    .category {
        font-size: 12px;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 5px;
    }
    .product-info h3 { font-size: 16px; margin-bottom: 6px; }
    .price { color: #d4a84b; font-weight: 700; font-size: 17px; }
    footer {
        background: #111;
        color: #aaa;
        text-align: center;
        padding: 40px 20px;
        margin-top: 70px;
    }
    footer .logo { margin-bottom: 12px; display: inline-block; }
    .detail-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 50px;
        max-width: 1100px;
        margin: 50px auto;
        padding: 0 20px;
        align-items: center;
    }
    .detail-img {
        height: 480px;
        background-size: cover;
        background-position: center;
        border-radius: 12px;
    }
    .detail-info h1 { font-size: 30px; margin-bottom: 10px; }
    .detail-info .price { font-size: 26px; margin: 15px 0; }
    .detail-info p { color: #555; margin-bottom: 25px; }
    .cart-table {
        width: 100%;
        border-collapse: collapse;
        background: white;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 14px rgba(0,0,0,0.07);
    }
    .cart-table th, .cart-table td {
        padding: 16px;
        text-align: left;
        border-bottom: 1px solid #eee;
    }
    .cart-table th { background: #111; color: white; }
    .cart-total {
        text-align: right;
        font-size: 22px;
        font-weight: 700;
        margin-top: 25px;
    }
    .form-box {
        max-width: 550px;
        margin: 0 auto;
        background: white;
        padding: 35px;
        border-radius: 12px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.07);
    }
    .form-box input, .form-box textarea {
        width: 100%;
        padding: 12px 15px;
        margin-bottom: 18px;
        border: 1px solid #ddd;
        border-radius: 6px;
        font-size: 15px;
    }
    .form-box textarea { height: 130px; resize: vertical; }
    .success {
        background: #d4edda;
        color: #155724;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 25px;
    }
    .empty-cart {
        text-align: center;
        padding: 60px 20px;
        color: #666;
    }
    @media (max-width: 768px) {
        .detail-container { grid-template-columns: 1fr; }
        .detail-img { height: 350px; }
        header { padding: 14px 20px; }
        nav a { margin-left: 14px; font-size: 14px; }
    }
</style>
"""

def get_cart_count():
    cart = session.get("cart", {})
    return sum(cart.values())

def navbar():
    count = get_cart_count()
    return f"""
    <header>
        <div class="logo">R<span>&</span>M</div>
        <nav>
            <a href="/">Home</a>
            <a href="/products">Shop</a>
            <a href="/about">About</a>
            <a href="/contact">Contact</a>
            <a href="/cart">Cart <span class="cart-count">{count}</span></a>
        </nav>
    </header>
    """

@app.route("/")
def home():
    featured = list(products.items())[:8]
    cards = ""
    for pid, p in featured:
        cards += f"""
        <a href="/product/{pid}" class="product-card">
            <div class="product-img" style="background-image: url('{p['image']}')"></div>
            <div class="product-info">
                <div class="category">{p['category']}</div>
                <h3>{p['name']}</h3>
                <div class="price">₹{p['price']}</div>
            </div>
        </a>
        """
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>R&M | Premium Clothing</title>
        {BASE_STYLE}
    </head>
    <body>
        {navbar()}
        <section class="hero">
            <h1>R&M Clothing</h1>
            <p>From everyday essentials to luxury fashion</p>
            <a href="/products" class="btn">Shop Collection</a>
        </section>
        <section class="section">
            <h2>Featured Products</h2>
            <div class="products">{cards}</div>
        </section>
        <footer>
            <div class="logo">R<span>&</span>M</div>
            <p>© 2026 R&M Clothing. All rights reserved.</p>
        </footer>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route("/products")
def products_page():
    cards = ""
    for pid, p in products.items():
        cards += f"""
        <a href="/product/{pid}" class="product-card">
            <div class="product-img" style="background-image: url('{p['image']}')"></div>
            <div class="product-info">
                <div class="category">{p['category']}</div>
                <h3>{p['name']}</h3>
                <div class="price">₹{p['price']}</div>
            </div>
        </a>
        """
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Shop | R&M</title>
        {BASE_STYLE}
    </head>
    <body>
        {navbar()}
        <section class="section" style="margin-top:40px;">
            <h2>Our Full Collection</h2>
            <div class="products">{cards}</div>
        </section>
        <footer>
            <div class="logo">R<span>&</span>M</div>
            <p>© 2026 R&M Clothing. All rights reserved.</p>
        </footer>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route("/product/<int:pid>")
def product_detail(pid):
    p = products.get(pid)
    if not p:
        return redirect(url_for("products_page"))
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{p['name']} | R&M</title>
        {BASE_STYLE}
    </head>
    <body>
        {navbar()}
        <div class="detail-container">
            <div class="detail-img" style="background-image: url('{p['image']}')"></div>
            <div class="detail-info">
                <div class="category">{p['category']}</div>
                <h1>{p['name']}</h1>
                <div class="price">₹{p['price']}</div>
                <p>{p['desc']}</p>
                <form action="/add_to_cart/{pid}" method="POST" style="display:inline;">
                    <button type="submit" class="btn">Add to Cart</button>
                </form>
                <a href="/products" class="btn btn-outline" style="margin-left:12px;">Back to Shop</a>
            </div>
        </div>
        <footer>
            <div class="logo">R<span>&</span>M</div>
            <p>© 2026 R&M Clothing. All rights reserved.</p>
        </footer>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route("/add_to_cart/<int:pid>", methods=["POST"])
def add_to_cart(pid):
    if pid not in products:
        return redirect(url_for("products_page"))
    cart = session.get("cart", {})
    cart[str(pid)] = cart.get(str(pid), 0) + 1
    session["cart"] = cart
    return redirect(url_for("cart"))

@app.route("/remove_from_cart/<int:pid>")
def remove_from_cart(pid):
    cart = session.get("cart", {})
    if str(pid) in cart:
        del cart[str(pid)]
        session["cart"] = cart
    return redirect(url_for("cart"))

@app.route("/cart")
def cart():
    cart = session.get("cart", {})
    items = []
    total = 0
    for pid_str, qty in cart.items():
        pid = int(pid_str)
        if pid in products:
            p = products[pid]
            subtotal = p["price"] * qty
            total += subtotal
            items.append({
                "id": pid,
                "name": p["name"],
                "price": p["price"],
                "qty": qty,
                "subtotal": subtotal,
                "image": p["image"]
            })

    rows = ""
    if items:
        for item in items:
            rows += f"""
            <tr>
                <td>
                    <div style="display:flex;align-items:center;gap:15px;">
                        <div style="width:60px;height:60px;background-image:url('{item['image']}');background-size:cover;background-position:center;border-radius:6px;"></div>
                        {item['name']}
                    </div>
                </td>
                <td>₹{item['price']}</td>
                <td>{item['qty']}</td>
                <td>₹{item['subtotal']}</td>
                <td><a href="/remove_from_cart/{item['id']}" style="color:#c0392b;text-decoration:none;font-weight:600;">Remove</a></td>
            </tr>
            """
        content = f"""
        <table class="cart-table">
            <thead>
                <tr>
                    <th>Product</th>
                    <th>Price</th>
                    <th>Qty</th>
                    <th>Subtotal</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>{rows}</tbody>
        </table>
        <div class="cart-total">Total: ₹{total}</div>
        <div style="text-align:right;margin-top:25px;">
            <a href="/products" class="btn btn-outline" style="margin-right:12px;">Continue Shopping</a>
            <a href="/contact" class="btn">Proceed to Checkout</a>
        </div>
        """
    else:
        content = """
        <div class="empty-cart">
            <h3>Your cart is empty</h3>
            <p style="margin:15px 0 25px;">Looks like you haven't added anything yet.</p>
            <a href="/products" class="btn">Start Shopping</a>
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cart | R&M</title>
        {BASE_STYLE}
    </head>
    <body>
        {navbar()}
        <section class="section" style="margin-top:40px;">
            <h2>Your Cart</h2>
            {content}
        </section>
        <footer>
            <div class="logo">R<span>&</span>M</div>
            <p>© 2026 R&M Clothing. All rights reserved.</p>
        </footer>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route("/about")
def about():
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>About | R&M</title>
        {BASE_STYLE}
    </head>
    <body>
        {navbar()}
        <section class="section" style="margin-top:60px;">
            <h2>About R&M</h2>
            <div style="max-width:750px;margin:0 auto;text-align:center;font-size:17px;color:#444;">
                <p style="margin-bottom:20px;">
                    R&M brings you fashion for everyone — from affordable everyday wear to premium luxury pieces.
                </p>
                <p style="margin-bottom:20px;">
                    We believe good style should be accessible. Whether you want budget-friendly essentials or high-end fashion, R&M has something for you.
                </p>
                <a href="/products" class="btn">Explore Collection</a>
            </div>
        </section>
        <footer>
            <div class="logo">R<span>&</span>M</div>
            <p>© 2026 R&M Clothing. All rights reserved.</p>
        </footer>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    success = False
    if request.method == "POST":
        success = True

    form_html = ""
    if success:
        form_html = '<div class="success">Thank you! Your message has been sent. We will contact you soon.</div>'

    form_html += """
    <div class="form-box">
        <form method="POST">
            <input type="text" name="name" placeholder="Your Name" required>
            <input type="email" name="email" placeholder="Your Email" required>
            <input type="text" name="subject" placeholder="Subject" required>
            <textarea name="message" placeholder="Your Message" required></textarea>
            <button type="submit" class="btn" style="width:100%;">Send Message</button>
        </form>
    </div>
    """

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Contact | R&M</title>
        {BASE_STYLE}
    </head>
    <body>
        {navbar()}
        <section class="section" style="margin-top:50px;">
            <h2>Contact Us</h2>
            {form_html}
        </section>
        <footer>
            <div class="logo">R<span>&</span>M</div>
            <p>© 2026 R&M Clothing. All rights reserved.</p>
        </footer>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
