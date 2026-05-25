---
name: Super900 Elite
colors:
  surface: '#121414'
  surface-dim: '#121414'
  surface-bright: '#37393a'
  surface-container-lowest: '#0c0f0f'
  surface-container-low: '#1a1c1c'
  surface-container: '#1e2020'
  surface-container-high: '#282a2b'
  surface-container-highest: '#333535'
  on-surface: '#e2e2e2'
  on-surface-variant: '#c3c6d2'
  inverse-surface: '#e2e2e2'
  inverse-on-surface: '#2f3131'
  outline: '#8d909c'
  outline-variant: '#434751'
  surface-tint: '#acc7ff'
  primary: '#acc7ff'
  on-primary: '#002f67'
  primary-container: '#003e84'
  on-primary-container: '#83acf9'
  inverse-primary: '#315da5'
  secondary: '#ffb866'
  on-secondary: '#482900'
  secondary-container: '#f19700'
  on-secondary-container: '#5d3700'
  tertiary: '#bac7e3'
  on-tertiary: '#243147'
  tertiary-container: '#334057'
  on-tertiary-container: '#9facc7'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#d7e2ff'
  primary-fixed-dim: '#acc7ff'
  on-primary-fixed: '#001a40'
  on-primary-fixed-variant: '#0f458b'
  secondary-fixed: '#ffddba'
  secondary-fixed-dim: '#ffb866'
  on-secondary-fixed: '#2b1700'
  on-secondary-fixed-variant: '#673d00'
  tertiary-fixed: '#d6e3ff'
  tertiary-fixed-dim: '#bac7e3'
  on-tertiary-fixed: '#0e1c31'
  on-tertiary-fixed-variant: '#3a475e'
  background: '#121414'
  on-background: '#e2e2e2'
  surface-variant: '#333535'
  deep-black: '#000000'
  charcoal-surface: '#121212'
  glass-border: rgba(255, 255, 255, 0.12)
  success-green: '#28C76F'
  error-red: '#EA5455'
typography:
  display-lg:
    fontFamily: Montserrat
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Montserrat
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
  headline-lg-mobile:
    fontFamily: Montserrat
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
  headline-md:
    fontFamily: Montserrat
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  container-max-width: 1280px
  gutter-desktop: 24px
  gutter-mobile: 16px
  margin-desktop: 40px
  margin-mobile: 20px
---

## Brand & Style

The design system is engineered for a premium supermarket delivery experience that mirrors the exclusivity of a high-end physical boutique. The target audience consists of discerning urban professionals who value efficiency, quality, and a curated shopping environment. 

The aesthetic is **Minimalist-Glassmorphic**. It leverages a "Lights Out" dark mode foundation where depth is created through varying levels of charcoal surfaces and frosted glass overlays rather than traditional shadows. The interface feels luxurious yet highly functional, emphasizing vibrant food photography against a somber, sophisticated backdrop. The emotional response is one of trust, precision, and culinary excellence.

## Colors

The palette is anchored by **Deep Black (#000000)** for primary backgrounds to provide maximum contrast for product photography. 

- **Primary Blue (#003E84):** Used for primary actions, selection states, and brand iconography. It conveys reliability and corporate maturity.
- **Secondary Gold (#FEA116):** Used sparingly as an accent for highlights, "Express" delivery tags, and star ratings. It provides a premium, "golden-hour" warmth.
- **Tertiary Dark Blue (#061429):** Utilized for secondary surface containers and card backgrounds to soften the transition from absolute black.
- **Neutral White (#FFFFFF):** Reserved strictly for high-readability text and icons. Never used as a background element.

## Typography

Typography prioritizes clarity and a structured hierarchy. **Montserrat** is used for headlines to provide a geometric, modern confidence. **Inter** is used for all functional body text and labels to ensure maximum legibility at small sizes, particularly for ingredient lists and price points.

For mobile devices, headline sizes scale down to prevent awkward line breaks. All text on dark backgrounds uses a subtle increase in tracking (letter-spacing) to combat the visual "bleeding" effect of white text on black.

## Layout & Spacing

The design system utilizes a **12-column fluid grid** for desktop and a **4-column grid** for mobile. The spacing rhythm is based on an 8px base unit.

- **Desktop:** Large margins (40px+) create an editorial feel, allowing high-quality imagery to breathe.
- **Mobile:** Margins are tighter (20px) to maximize the "shelf space" for product cards.
- **Vertical Spacing:** Generous padding between categories (section spacing of 64px-80px) reinforces the premium, un-cluttered brand positioning.

## Elevation & Depth

In this dark-themed system, elevation is conveyed through **Tonal Layering** and **Glassmorphism**:

1.  **Level 0 (Base):** Absolute Black (#000000).
2.  **Level 1 (Cards/Navigation):** Charcoal Surface (#121212) with a 1px `glass-border` at 12% opacity.
3.  **Level 2 (Modals/Pop-overs):** Backdrop blur (20px) with a semi-transparent fill of #1A1A1A at 80% opacity.
4.  **Shadows:** Shadows are rarely used. When necessary, they are large, highly diffused, and use #000000 with 50% opacity to "lift" elements off the charcoal surfaces without appearing muddy.

## Shapes

The shape language is consistently **Rounded**. This softens the "industrial" feel of the dark theme and makes the grocery shopping experience feel more approachable and modern.

- **Standard Elements (Buttons, Inputs):** 0.5rem (8px) radius.
- **Product Cards:** 1rem (16px) radius to create a distinct "container" look.
- **Banners & Featured Content:** 1.5rem (24px) radius for a bold, modern silhouette.

## Components

### Buttons
- **Primary:** Solid Primary Blue with White text. Bold weight.
- **Secondary:** Transparent with a 1px White border (Ghost style).
- **Add-to-Cart:** Secondary Gold background with Black text to create a high-contrast focal point that drives conversion.

### Premium Grocery Cards
Cards feature a Level 1 charcoal surface. Product imagery should have a consistent "studio" look with soft lighting. Price is displayed in Montserrat Bold. A "Quick Add" (+) button is anchored to the bottom right in Primary Blue.

### Search Bar
A high-visibility, level 2 glassmorphic input. It should occupy a prominent position at the top of the interface with a subtle inner glow to signify focus.

### Category Navigation
Uses rounded chips with Level 1 surfaces. When active, the chip transitions to Primary Blue with a subtle outer glow.

### Cart & Checkout
A side-drawer (mobile) or floating persistent panel (desktop) utilizing heavy backdrop blur. Item rows are separated by thin `glass-border` lines. The "Checkout" button is always pinned to the bottom of the viewport for immediate access.