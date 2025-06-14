import streamlit as st
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="MathCraft: Twisted Curves", layout="centered")

# Header
st.markdown("""
<div style='text-align: center;'>
    <h1 style='color:#4B0082;'>🧠 MathCraft</h1>
    <h2>Twisted Curves</h2>
    <p style='font-size: 1.1em;'>Built by Xavier Honablue, M.Ed</p>
</div>
<hr>
""", unsafe_allow_html=True)

# Helper function to create polynomial string from zeros
def zeros_to_polynomial_string(zeros):
    """Convert list of zeros to polynomial string representation"""
    if len(zeros) == 2:
        a, b = zeros
        # (x-a)(x-b) = x² - (a+b)x + ab
        coef_x2 = 1
        coef_x1 = -(a + b)
        coef_x0 = a * b
        
        terms = []
        if coef_x2 != 0:
            if coef_x2 == 1:
                terms.append("x^2")
            elif coef_x2 == -1:
                terms.append("-x^2")
            else:
                terms.append(f"{coef_x2}x^2")
        
        if coef_x1 != 0:
            if coef_x1 > 0 and terms:
                terms.append(f"+{coef_x1}x" if coef_x1 != 1 else "+x")
            elif coef_x1 < 0:
                terms.append(f"{coef_x1}x" if coef_x1 != -1 else "-x")
            else:
                terms.append("x" if coef_x1 == 1 else f"{coef_x1}x")
        
        if coef_x0 != 0:
            if coef_x0 > 0 and terms:
                terms.append(f"+{coef_x0}")
            else:
                terms.append(f"{coef_x0}")
        
        return "".join(terms) if terms else "0"
    
    elif len(zeros) == 3:
        a, b, c = zeros
        # (x-a)(x-b)(x-c) expanded
        coef_x3 = 1
        coef_x2 = -(a + b + c)
        coef_x1 = a*b + a*c + b*c
        coef_x0 = -a*b*c
        
        terms = []
        if coef_x3 != 0:
            terms.append("x^3" if coef_x3 == 1 else f"{coef_x3}x^3")
        
        if coef_x2 != 0:
            if coef_x2 > 0 and terms:
                terms.append(f"+{coef_x2}x^2" if coef_x2 != 1 else "+x^2")
            elif coef_x2 < 0:
                terms.append(f"{coef_x2}x^2" if coef_x2 != -1 else "-x^2")
            else:
                terms.append("x^2" if coef_x2 == 1 else f"{coef_x2}x^2")
        
        if coef_x1 != 0:
            if coef_x1 > 0 and terms:
                terms.append(f"+{coef_x1}x" if coef_x1 != 1 else "+x")
            elif coef_x1 < 0:
                terms.append(f"{coef_x1}x" if coef_x1 != -1 else "-x")
            else:
                terms.append("x" if coef_x1 == 1 else f"{coef_x1}x")
        
        if coef_x0 != 0:
            if coef_x0 > 0 and terms:
                terms.append(f"+{coef_x0}")
            else:
                terms.append(f"{coef_x0}")
        
        return "".join(terms) if terms else "0"
    
    elif len(zeros) == 4:
        # For 4 zeros, just show the factored form
        factor_terms = []
        for z in zeros:
            if z >= 0:
                factor_terms.append(f"(x-{z})")
            else:
                factor_terms.append(f"(x+{abs(z)})")
        return "".join(factor_terms)
    
    return "Complex polynomial"

# --- MODE SWITCH ---
st.subheader("🛠️ Choose Input Mode")
mode = st.radio("Do you want to control the graph using...", ["Zeros (roots)", "Polynomial coefficients"])

# --- ZEROS MODE ---
if mode == "Zeros (roots)":
    st.subheader("🎮 Move the Zeros - Watch the Polynomial Change")

    num_factors = st.selectbox("How many factors do you want?", [2, 3, 4], index=2)
    default_zeros = [-2.0, 1.0, 3.0, 4.0]
    zeros = []

    if st.button("🔄 Reset Zeros to Default"):
        st.rerun()

    for i in range(num_factors):
        zero = st.slider(f"Zero {i+1} (x = root_{i+1})", -5.0, 5.0, default_zeros[i], step=0.1)
        zeros.append(zero)

    # Generate polynomial from roots
    t = np.linspace(-6, 6, 400)
    f_t = np.ones_like(t)
    for z in zeros:
        f_t *= (t - z)

    # Display polynomial expression
    poly_string = zeros_to_polynomial_string(zeros)
    st.latex(f"f(x) = {poly_string}")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=f_t, mode='lines', name='f(x)', line=dict(width=3)))
    fig.add_trace(go.Scatter(x=zeros, y=[0]*len(zeros), mode='markers+text', name='Zeros',
                             marker=dict(size=10, color='red'),
                             text=[f"x = {round(z,1)}" for z in zeros],
                             textposition='top center'))
    fig.update_layout(title="Graph of f(x) = Product of (x - root)",
                      xaxis_title="x",
                      yaxis_title="f(x)",
                      height=500)
    st.plotly_chart(fig)

# --- COEFFICIENT MODE ---
else:
    st.subheader("✏️ Enter Coefficients of Your Polynomial")
    st.markdown("Enter the coefficients of your polynomial in standard form: \\( ax^3 + bx^2 + cx + d \\)")

    a = st.number_input("a (x³)", value=1.0, step=0.1)
    b = st.number_input("b (x²)", value=0.0, step=0.1)
    c = st.number_input("c (x¹)", value=0.0, step=0.1)
    d = st.number_input("d (constant)", value=0.0, step=0.1)

    # Define polynomial function
    t = np.linspace(-6, 6, 400)
    f_t = a*t**3 + b*t**2 + c*t + d

    # Display expression
    st.latex(f"f(x) = {a}x^3 + {b}x^2 + {c}x + {d}")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=f_t, mode='lines', name='f(x)', line=dict(width=3)))
    fig.update_layout(title="Graph of f(x) = ax³ + bx² + cx + d",
                      xaxis_title="x",
                      yaxis_title="f(x)",
                      height=500)
    st.plotly_chart(fig)

# --- Concept Check ---
st.subheader("🧠 Concept Check")
st.markdown("""
- **Zeros** are the x-values where the graph touches or crosses the x-axis.
- **Factors** are the algebraic expressions that produce these zeros.

For example:
- Zero at \\( x = 1 \\) → Factor is \\( (x - 1) \\)
- Zero at \\( x = -2 \\) → Factor is \\( (x + 2) \\)

They are connected, but not interchangeable.

🧪 **Challenge:** What factor corresponds to a zero at \\( x = 5 \\)?
""")

# --- EXTRA: Twisted S-Curve ---
st.markdown("""
<hr>
<h2 style='color:#4B0082;'>🌀 Bonus: Twisting the S-Curve</h2>
<p>What happens when we modify a simple cubic like \\( -x^3 \\) by adding a linear term like \\( +x \\)? Let's visualize it.</p>
""", unsafe_allow_html=True)

x = np.linspace(-4, 4, 400)
y1 = -x**3
y2 = -x**3 + x

fig2, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, y1, label=r"$f(x) = -x^3$", linestyle='--', color='orange', linewidth=2)
ax.plot(x, y2, label=r"$f(x) = -x^3 + x$", color='purple', linewidth=2)
ax.axhline(0, color='black', linewidth=0.5)
ax.axvline(0, color='black', linewidth=0.5)
ax.set_title("Visual Impact of Adding +x to $f(x) = -x^3$")
ax.set_xlabel("x")
ax.set_ylabel("f(x)")
ax.legend()
ax.grid(True)
st.pyplot(fig2)

st.markdown("""
- The **orange dashed** curve is the original \\( -x^3 \\), a mirrored S-shape.
- The **purple** curve shows \\( -x^3 + x \\), where the middle **twists**.

Think of it like this:
- The **bottom right** of the curve is **coming toward you**.
- The **top left** is **diving into the paper**.

A small term like \\( +x \\) creates major shape changes near the origin.
""")
