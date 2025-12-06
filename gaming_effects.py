"""
Gaming Effects Module - Epic visual effects for the dashboard
"""

import streamlit as st


def inject_particle_background():
    """Inject animated particle background effect (optional - can be heavy)"""
    st.markdown("""
    <div id="particles-js" style="
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        pointer-events: none;
    "></div>
    
    <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
    <script>
    particlesJS('particles-js', {
        particles: {
            number: { value: 80, density: { enable: true, value_area: 800 } },
            color: { value: ['#00ffff', '#ff00ff', '#00ff88'] },
            shape: { type: 'circle' },
            opacity: {
                value: 0.5,
                random: true,
                anim: { enable: true, speed: 1, opacity_min: 0.1, sync: false }
            },
            size: {
                value: 3,
                random: true,
                anim: { enable: true, speed: 2, size_min: 0.1, sync: false }
            },
            line_linked: {
                enable: true,
                distance: 150,
                color: '#00ffff',
                opacity: 0.4,
                width: 1
            },
            move: {
                enable: true,
                speed: 2,
                direction: 'none',
                random: false,
                straight: false,
                out_mode: 'out',
                bounce: false
            }
        },
        interactivity: {
            detect_on: 'canvas',
            events: {
                onhover: { enable: true, mode: 'repulse' },
                onclick: { enable: true, mode: 'push' },
                resize: true
            }
        },
        retina_detect: true
    });
    </script>
    """, unsafe_allow_html=True)


def inject_scanline_effect():
    """Inject retro CRT scanline effect"""
    st.markdown("""
    <style>
    /* CRT Scanline Effect */
    .main::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: repeating-linear-gradient(
            0deg,
            rgba(0, 0, 0, 0.15),
            rgba(0, 0, 0, 0.15) 1px,
            transparent 1px,
            transparent 2px
        );
        pointer-events: none;
        z-index: 1000;
        animation: scanline 8s linear infinite;
    }
    
    @keyframes scanline {
        0% { transform: translateY(0); }
        100% { transform: translateY(10px); }
    }
    </style>
    """, unsafe_allow_html=True)


def inject_glitch_effect():
    """Inject subtle glitch effect for headers"""
    st.markdown("""
    <style>
    /* Glitch Effect */
    @keyframes glitch {
        0% {
            text-shadow: 
                0.05em 0 0 rgba(255, 0, 0, 0.75),
                -0.05em -0.025em 0 rgba(0, 255, 0, 0.75),
                -0.025em 0.05em 0 rgba(0, 0, 255, 0.75);
        }
        14% {
            text-shadow: 
                0.05em 0 0 rgba(255, 0, 0, 0.75),
                -0.05em -0.025em 0 rgba(0, 255, 0, 0.75),
                -0.025em 0.05em 0 rgba(0, 0, 255, 0.75);
        }
        15% {
            text-shadow: 
                -0.05em -0.025em 0 rgba(255, 0, 0, 0.75),
                0.025em 0.025em 0 rgba(0, 255, 0, 0.75),
                -0.05em -0.05em 0 rgba(0, 0, 255, 0.75);
        }
        49% {
            text-shadow: 
                -0.05em -0.025em 0 rgba(255, 0, 0, 0.75),
                0.025em 0.025em 0 rgba(0, 255, 0, 0.75),
                -0.05em -0.05em 0 rgba(0, 0, 255, 0.75);
        }
        50% {
            text-shadow: 
                0.025em 0.05em 0 rgba(255, 0, 0, 0.75),
                0.05em 0 0 rgba(0, 255, 0, 0.75),
                0 -0.05em 0 rgba(0, 0, 255, 0.75);
        }
        99% {
            text-shadow: 
                0.025em 0.05em 0 rgba(255, 0, 0, 0.75),
                0.05em 0 0 rgba(0, 255, 0, 0.75),
                0 -0.05em 0 rgba(0, 0, 255, 0.75);
        }
        100% {
            text-shadow: 
                -0.025em 0 0 rgba(255, 0, 0, 0.75),
                -0.025em -0.025em 0 rgba(0, 255, 0, 0.75),
                -0.025em -0.05em 0 rgba(0, 0, 255, 0.75);
        }
    }
    
    /* Apply glitch to specific elements occasionally */
    h1:hover {
        animation: glitch 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94) both;
    }
    </style>
    """, unsafe_allow_html=True)


def create_level_badge(level_number: int, level_name: str, color: str = "#00ffff") -> str:
    """
    Create a gaming-style level badge
    
    Args:
        level_number: The level number
        level_name: Name of the level
        color: Hex color for the badge
        
    Returns:
        HTML string for the level badge
    """
    return f"""
    <div style='
        display: inline-block;
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.2) 0%, rgba(255, 0, 255, 0.2) 100%);
        border: 2px solid {color};
        border-radius: 10px;
        padding: 0.5rem 1.5rem;
        margin: 0.5rem;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.4);
        font-family: "Orbitron", sans-serif;
        font-weight: 700;
        letter-spacing: 2px;
    '>
        <span style='color: {color}; font-size: 1.2rem;'>
            LEVEL {level_number}
        </span>
        <span style='color: white; font-size: 1rem; margin-left: 0.5rem;'>
            {level_name}
        </span>
    </div>
    """


def create_achievement_badge(achievement_text: str, icon: str = "🏆") -> str:
    """
    Create a gaming-style achievement badge
    
    Args:
        achievement_text: The achievement description
        icon: Emoji icon for the achievement
        
    Returns:
        HTML string for the achievement badge
    """
    return f"""
    <div style='
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.2) 0%, rgba(255, 140, 0, 0.2) 100%);
        border: 2px solid #ffd700;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 0 25px rgba(255, 215, 0, 0.4);
        font-family: "Rajdhani", sans-serif;
        display: flex;
        align-items: center;
        gap: 1rem;
        transition: all 0.3s ease;
    ' onmouseover='this.style.transform="scale(1.05)"' onmouseout='this.style.transform="scale(1)"'>
        <span style='font-size: 2rem;'>{icon}</span>
        <div>
            <div style='color: #ffd700; font-weight: 700; font-size: 1.1rem; letter-spacing: 1px;'>
                ACHIEVEMENT UNLOCKED!
            </div>
            <div style='color: white; font-weight: 500; font-size: 1rem;'>
                {achievement_text}
            </div>
        </div>
    </div>
    """


def create_stat_bar(label: str, value: float, max_value: float, color: str = "#00ffff") -> str:
    """
    Create a gaming-style stat bar (like HP/MP bars)
    
    Args:
        label: Label for the stat
        value: Current value
        max_value: Maximum value
        color: Hex color for the bar
        
    Returns:
        HTML string for the stat bar
    """
    percentage = (value / max_value) * 100 if max_value > 0 else 0
    
    return f"""
    <div style='margin: 1rem 0;'>
        <div style='
            font-family: "Rajdhani", sans-serif;
            color: white;
            font-weight: 600;
            font-size: 1rem;
            margin-bottom: 0.5rem;
            letter-spacing: 1px;
        '>
            {label}: {value:.1f} / {max_value:.1f}
        </div>
        <div style='
            width: 100%;
            height: 25px;
            background: rgba(0, 0, 0, 0.5);
            border: 2px solid {color};
            border-radius: 5px;
            overflow: hidden;
            box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.5);
        '>
            <div style='
                width: {percentage}%;
                height: 100%;
                background: linear-gradient(90deg, {color} 0%, {color}dd 100%);
                box-shadow: 0 0 10px {color};
                transition: width 0.5s ease;
                position: relative;
            '>
                <div style='
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: linear-gradient(
                        90deg,
                        transparent 0%,
                        rgba(255, 255, 255, 0.3) 50%,
                        transparent 100%
                    );
                    animation: shimmer 2s infinite;
                '></div>
            </div>
        </div>
    </div>
    
    <style>
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    </style>
    """
