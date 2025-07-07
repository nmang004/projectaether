# Project Aether Design System

A sophisticated, modern design language for a ground-breaking application experience.

## Color Palette

### Primary Action
- **Gradient**: Linear gradient from #6D28D9 (deep violet) to #BE185D (fuchsia)
- **Usage**: Primary buttons, key calls-to-action, active states
- **CSS**: `background: linear-gradient(135deg, #6D28D9 0%, #BE185D 100%)`
- **Tailwind Class**: `bg-gradient-primary`

### Secondary Action
- **Color**: #F8F8F8 (off-white)
- **Border**: #E5E5E5 (1px fine border)
- **Usage**: Secondary buttons, alternative actions
- **CSS**: `background: #F8F8F8; border: 1px solid #E5E5E5`
- **Tailwind Class**: `bg-secondary-action border-secondary-border`

### Background
- **Color**: #F9FAFB (very light gray)
- **Usage**: Main application background, page backgrounds
- **Tailwind Class**: `bg-app-background`

### Accent
- **Color**: #F59E0B (amber)
- **Usage**: Highlights, notifications, active states, focus rings
- **Tailwind Class**: `bg-accent`

### Text Colors
- **Primary**: #1F2937 (dark charcoal)
- **Secondary**: #6B7280 (lighter gray)
- **Usage**: Primary for main content, secondary for subheadings and supporting text
- **Tailwind Classes**: `text-primary`, `text-secondary`

### Glassmorphism Colors
- **Background**: rgba(255, 255, 255, 0.7)
- **Border**: rgba(255, 255, 255, 0.2)
- **Backdrop Filter**: blur(12px)

## Typography

### Font Family
- **Primary**: 'Inter', system-ui, sans-serif
- **Import**: Google Fonts - Inter (weights: 400, 500, 600, 700)

### Font Weights
- **Regular**: 400 (font-normal)
- **Medium**: 500 (font-medium)
- **Semibold**: 600 (font-semibold)
- **Bold**: 700 (font-bold)

### Headlines (h1, h2, h3)
- **Weight**: Bold (font-bold)
- **Letter Spacing**: Tight (tracking-tight)
- **Line Height**: Tight (leading-tight)

### Body Copy
- **Weight**: Regular (font-normal)
- **Line Height**: Relaxed (leading-relaxed)

### Fluid Typography Scale
- **H1**: clamp(2rem, 4vw, 3rem)
- **H2**: clamp(1.5rem, 3vw, 2.25rem)
- **H3**: clamp(1.25rem, 2.5vw, 1.875rem)
- **Body**: clamp(0.875rem, 2vw, 1rem)
- **Small**: clamp(0.75rem, 1.5vw, 0.875rem)

## Spacing and Layout

### Spacing Scale (4px grid system)
- **space-1**: 4px
- **space-2**: 8px
- **space-3**: 12px
- **space-4**: 16px
- **space-6**: 24px
- **space-8**: 32px
- **space-12**: 48px
- **space-16**: 64px
- **space-24**: 96px

### Layout Standards
- **Max Width**: 1280px (max-w-7xl)
- **Container Padding**: 24px (px-6)
- **Content Alignment**: Centered
- **Section Spacing**: 48px (space-y-12)

## Component Styling

### Glassmorphism Effect
```css
.glassmorphism {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
}
```

### Shadow System
- **shadow-soft**: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.06)
- **shadow-lifted**: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)
- **shadow-dramatic**: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)

### Border Radius
- **Standard**: 12px (rounded-xl)
- **Small**: 8px (rounded-lg)
- **Large**: 16px (rounded-2xl)
- **Pill**: 9999px (rounded-full)

## Button Specifications

### Primary Button
- **Background**: Primary action gradient
- **Text**: White (#FFFFFF)
- **Shadow**: shadow-soft
- **Border Radius**: 12px
- **Padding**: 12px 24px
- **Font Weight**: Medium (font-medium)
- **Hover**: Gradient angle shift + shadow-lifted
- **Active**: More pronounced shadow-dramatic

### Secondary Button
- **Background**: #F8F8F8
- **Border**: 1px solid #E5E5E5
- **Text**: Primary text color (#1F2937)
- **Shadow**: None (initially)
- **Hover**: shadow-soft
- **Border Radius**: 12px
- **Padding**: 12px 24px

## Form Elements

### Input Fields
- **Background**: White
- **Border**: 1px solid #E5E5E5
- **Border Radius**: 12px
- **Padding**: 12px 16px
- **Focus**: Accent color border + shadow-soft
- **Placeholder**: Secondary text color

### Labels
- **Color**: Secondary text (#6B7280)
- **Font Weight**: Medium (font-medium)
- **Font Size**: Small (text-sm)
- **Margin Bottom**: 8px

## Navigation & Sidebar

### Glassmorphism Sidebar
- **Background**: Glassmorphism effect
- **Width**: 280px
- **Position**: Fixed left
- **Padding**: 24px

### Navigation Links
- **Active**: Pill-shaped background with primary gradient + white text
- **Inactive**: Secondary text color
- **Hover**: Subtle background (rgba(255, 255, 255, 0.5)) + slight scale transform
- **Padding**: 12px 20px
- **Border Radius**: 8px (pill-shaped)

## Charts and Data Visualization

### Color Palette
- **Primary Series**: Primary action gradient
- **Secondary Series**: Accent color (#F59E0B)
- **Tertiary Series**: #8B5CF6 (purple)
- **Background**: White or glassmorphism
- **Grid Lines**: #F3F4F6
- **Text**: Secondary text color

### Interactive Elements
- **Tooltips**: Glassmorphism background
- **Hover States**: Subtle glow effect
- **Animation**: Smooth transitions (300ms ease-in-out)

## Micro-interactions

### On-Load Animations
- **Fade In**: opacity: 0 → 1 (300ms ease-out)
- **Slide Up**: transform: translateY(20px) → translateY(0) (400ms ease-out)
- **Stagger Delay**: 100ms between elements

### Hover Effects
- **Cards**: transform: translateY(-4px) + shadow-lifted
- **Buttons**: Scale: 1.02 + shadow enhancement
- **Links**: Subtle color transition (200ms ease-in-out)

### Focus States
- **Ring**: 2px solid accent color
- **Ring Offset**: 2px
- **Transition**: All focus changes 150ms ease-in-out

## Layout Patterns

### Bento Grid
- **Gap**: 24px
- **Min Height**: 200px for cards
- **Responsive**: CSS Grid with auto-fit
- **Card Padding**: 24px

### Dashboard Widgets
- **Background**: White or glassmorphism
- **Border Radius**: 16px
- **Shadow**: shadow-soft
- **Hover**: shadow-lifted + translateY(-2px)

## Responsive Design

### Breakpoints
- **sm**: 640px
- **md**: 768px
- **lg**: 1024px
- **xl**: 1280px
- **2xl**: 1536px

### Mobile Optimizations
- **Touch Targets**: Minimum 44px
- **Font Scaling**: Fluid typography
- **Spacing**: Reduced on smaller screens
- **Navigation**: Collapsible sidebar

## Implementation Notes

### CSS Custom Properties
All colors and spacing values should be defined as CSS custom properties for easy theming and consistency.

### Performance
- Use `transform` and `opacity` for animations (GPU acceleration)
- Implement `will-change` property sparingly
- Preload critical fonts

### Accessibility
- Maintain WCAG 2.1 AA contrast ratios
- Ensure focus indicators are visible
- Provide reduced motion alternatives
- Use semantic HTML structure