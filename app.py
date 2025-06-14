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

# Common Core Standards & Resources
st.markdown("""
### 📚 **Common Core Standards Alignment**
- **A-APR.B.3**: Identify zeros of polynomials when suitable factorizations are available
- **F-IF.C.7c**: Graph polynomial functions, identifying zeros when suitable factorizations are available
- **A-SSE.A.2**: Use the structure of an expression to identify ways to rewrite it

### 🔗 **Additional Resources**
- 📖 [Khan Academy: Polynomial Factors and Graphs](https://www.khanacademy.org/math/algebra2/x2ec2f6f830c9fb89:poly-graphs)
- 🎯 [IXL: Find the roots of factored polynomials](https://www.ixl.com/math/algebra-2/find-the-roots-of-factored-polynomials)
- 📊 [Khan Academy: Zeros of polynomials](https://www.khanacademy.org/math/algebra2/x2ec2f6f830c9fb89:poly-graphs/x2ec2f6f830c9fb89:zeros-of-polynomials/v/polynomial-zeros-introduction)
""", unsafe_allow_html=True)

# Helper function to create polynomial string from zeros
def zeros_to_polynomial_string(zeros):
    """Convert list of zeros to clean polynomial string representation"""
    
    def format_coefficient(coef, power, is_first=False):
        """Format a single term with proper signs and spacing"""
        if coef == 0:
            return ""
        
        # Handle the coefficient
        if power == 0:  # Constant term
            if coef > 0 and not is_first:
                return f" + {coef:g}"
            else:
                return f"{coef:g}"
        elif power == 1:  # Linear term
            if coef == 1:
                coef_str = "" if is_first else " + "
            elif coef == -1:
                coef_str = "-" if is_first else " - "
            elif coef > 0:
                coef_str = f"{coef:g}" if is_first else f" + {coef:g}"
            else:
                coef_str = f"{coef:g}" if is_first else f" - {abs(coef):g}"
            return f"{coef_str}x"
        else:  # Higher powers
            if coef == 1:
                coef_str = "" if is_first else " + "
            elif coef == -1:
                coef_str = "-" if is_first else " - "
            elif coef > 0:
                coef_str = f"{coef:g}" if is_first else f" + {coef:g}"
            else:
                coef_str = f"{coef:g}" if is_first else f" - {abs(coef):g}"
            return f"{coef_str}x^{power}"
    
    if len(zeros) == 2:
        a, b = zeros
        # (x-a)(x-b) = x² - (a+b)x + ab
        coef_x2 = 1
        coef_x1 = -(a + b)
        coef_x0 = a * b
        
        terms = []
        terms.append(format_coefficient(coef_x2, 2, True))
        if coef_x1 != 0:
            terms.append(format_coefficient(coef_x1, 1))
        if coef_x0 != 0:
            terms.append(format_coefficient(coef_x0, 0))
        
        return "".join(terms) if any(terms) else "0"
    
    elif len(zeros) == 3:
        a, b, c = zeros
        # (x-a)(x-b)(x-c) expanded
        coef_x3 = 1
        coef_x2 = -(a + b + c)
        coef_x1 = a*b + a*c + b*c
        coef_x0 = -a*b*c
        
        terms = []
        terms.append(format_coefficient(coef_x3, 3, True))
        if coef_x2 != 0:
            terms.append(format_coefficient(coef_x2, 2))
        if coef_x1 != 0:
            terms.append(format_coefficient(coef_x1, 1))
        if coef_x0 != 0:
            terms.append(format_coefficient(coef_x0, 0))
        
        return "".join(terms) if any(terms) else "0"
    
    elif len(zeros) == 4:
        # For 4 zeros, show clean factored form
        factor_terms = []
        for z in zeros:
            if z == 0:
                factor_terms.append("x")
            elif z > 0:
                factor_terms.append(f"(x - {z:g})")
            else:
                factor_terms.append(f"(x + {abs(z):g})")
        return "".join(factor_terms)
    
    return "f(x)"

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
        zero = st.slider(f"Zero {i+1}", -5.0, 5.0, default_zeros[i], step=0.1)
        st.latex(f"x = {zero:g}")
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
                             marker=dict(size=12, color='red', symbol='circle'),
                             text=[f"x = {z:g}" for z in zeros],
                             textposition='top center',
                             textfont=dict(size=14, color='red')))
    fig.update_layout(title="Graph of f(x) = Product of (x - root)",
                      xaxis_title="x",
                      yaxis_title="f(x)",
                      height=500)
    st.plotly_chart(fig)

# --- COEFFICIENT MODE ---
else:
    st.subheader("✏️ Enter Coefficients of Your Polynomial")
    st.markdown("Enter the coefficients of your polynomial in standard form:")
    st.latex(r"f(x) = ax^3 + bx^2 + cx + d")

    # Use sliders for real-time updates instead of number inputs
    col1, col2 = st.columns(2)
    
    with col1:
        a = st.slider("a", min_value=-5.0, max_value=5.0, value=1.4, step=0.1, key="coef_a")
        st.latex(f"a = {a:g}")
        c = st.slider("c", min_value=-5.0, max_value=5.0, value=0.9, step=0.1, key="coef_c")
        st.latex(f"c = {c:g}")
    
    with col2:
        b = st.slider("b", min_value=-5.0, max_value=5.0, value=1.4, step=0.1, key="coef_b")
        st.latex(f"b = {b:g}")
        d = st.slider("d", min_value=-10.0, max_value=10.0, value=4.7, step=0.1, key="coef_d")
        st.latex(f"d = {d:g}")

    # Pre-compute x values once for performance
    if 'x_values' not in st.session_state:
        st.session_state.x_values = np.linspace(-6, 6, 400)
    
    t = st.session_state.x_values
    f_t = a*t**3 + b*t**2 + c*t + d

    # Display expression with better formatting
    def format_polynomial_display(a, b, c, d):
        """Format polynomial coefficients into clean mathematical expression"""
        terms = []
        
        # x³ term
        if a != 0:
            if a == 1:
                terms.append("x^3")
            elif a == -1:
                terms.append("-x^3")
            else:
                terms.append(f"{a:g}x^3")
        
        # x² term
        if b != 0:
            if b > 0 and terms:
                if b == 1:
                    terms.append(" + x^2")
                else:
                    terms.append(f" + {b:g}x^2")
            elif b < 0:
                if b == -1:
                    terms.append(" - x^2")
                else:
                    terms.append(f" - {abs(b):g}x^2")
            else:  # b != 0 and no existing terms
                if b == 1:
                    terms.append("x^2")
                else:
                    terms.append(f"{b:g}x^2")
        
        # x term
        if c != 0:
            if c > 0 and terms:
                if c == 1:
                    terms.append(" + x")
                else:
                    terms.append(f" + {c:g}x")
            elif c < 0:
                if c == -1:
                    terms.append(" - x")
                else:
                    terms.append(f" - {abs(c):g}x")
            else:  # c != 0 and no existing terms
                if c == 1:
                    terms.append("x")
                else:
                    terms.append(f"{c:g}x")
        
        # constant term
        if d != 0:
            if d > 0 and terms:
                terms.append(f" + {d:g}")
            elif d < 0:
                terms.append(f" - {abs(d):g}")
            else:  # d != 0 and no existing terms
                terms.append(f"{d:g}")
        
        result = "".join(terms) if terms else "0"
        return result
    
    polynomial_display = format_polynomial_display(a, b, c, d)
    st.latex(f"f(x) = {polynomial_display}")

    # Optimized plotting with fixed layout for performance
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=t, 
        y=f_t, 
        mode='lines', 
        name='f(x)', 
        line=dict(width=3, color='#1f77b4')
    ))
    
    # Fixed layout prevents constant rescaling
    fig.update_layout(
        title="Graph of f(x) = ax³ + bx² + cx + d",
        xaxis_title="x",
        yaxis_title="f(x)",
        height=500,
        xaxis=dict(range=[-6, 6]),
        yaxis=dict(range=[-300, 300]),
        showlegend=False
    )
    
    # Use container for smooth updates
    chart_container = st.empty()
    chart_container.plotly_chart(fig, use_container_width=True)

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

### 📚 **Practice More:**
- 🎯 [IXL: Factor polynomials using the GCF](https://www.ixl.com/math/algebra-1/factor-polynomials-using-the-gcf)
- 📖 [Khan Academy: Factoring polynomials by grouping](https://www.khanacademy.org/math/algebra/x2f8bb11595b61c86:quadratics-multiplying-factoring/x2f8bb11595b61c86:factoring-quadratics-2/v/factoring-by-grouping)
- 🎯 [IXL: Solve polynomial equations](https://www.ixl.com/math/algebra-2/solve-polynomial-equations)
""")

# Common Core alignment for this section
st.markdown("""
<div style='background-color: #f0f8ff; padding: 10px; border-radius: 5px; margin: 10px 0;'>
<strong>📋 Standards:</strong> A-APR.B.3, A-SSE.A.2 - Understanding the relationship between factors and zeros
</div>
""", unsafe_allow_html=True)

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
""")

st.latex(r"\text{A small term like } +x \text{ creates major shape changes near the origin.}")

st.markdown("""
### 🎓 **Explore Further:**
- 📖 [Khan Academy: Transforming polynomial functions](https://www.khanacademy.org/math/algebra2/x2ec2f6f830c9fb89:poly-graphs/x2ec2f6f830c9fb89:poly-end-behavior/v/polynomial-end-behavior)
- 🎯 [IXL: Graph polynomial functions](https://www.ixl.com/math/algebra-2/graph-polynomial-functions)
- 📊 [Khan Academy: End behavior of polynomial functions](https://www.khanacademy.org/math/algebra2/x2ec2f6f830c9fb89:poly-graphs/x2ec2f6f830c9fb89:poly-end-behavior/v/polynomial-end-behavior)
""")

# Clean standards box - properly formatted
st.markdown("""
<div style='background-color: #f0f8ff; padding: 15px; border-radius: 8px; margin: 15px 0; border-left: 4px solid #4B0082;'>
<h4 style='margin-top: 0; color: #2c3e50; font-family: serif;'>📋 Standards Alignment</h4>
</div>
""", unsafe_allow_html=True)

st.latex(r"\textbf{F-IF.C.7c:} \text{ Graph polynomial functions, identifying zeros and end behavior}")
st.latex(r"\textbf{A-APR.A.1:} \text{ Understand that polynomials form a system analogous to the integers}")  
st.latex(r"\textbf{F-BF.B.3:} \text{ Identify the effect on the graph of replacing } f(x) \text{ by } f(x) + k")
