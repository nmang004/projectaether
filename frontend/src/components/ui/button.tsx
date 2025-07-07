import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center whitespace-nowrap rounded-xl text-sm font-medium transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 font-inter",
  {
    variants: {
      variant: {
        default: "bg-gradient-primary text-white shadow-soft hover:bg-gradient-primary-hover hover:shadow-lifted hover:scale-[1.02] active:shadow-dramatic",
        destructive:
          "bg-destructive text-destructive-foreground hover:bg-destructive/90 shadow-soft hover:shadow-lifted",
        outline:
          "border border-secondary-border bg-secondary-action text-text-primary hover:shadow-soft hover:scale-[1.02] active:shadow-lifted",
        secondary:
          "bg-secondary-action text-text-primary border border-secondary-border hover:shadow-soft hover:scale-[1.02]",
        ghost: "hover:bg-secondary-action hover:text-text-primary hover:scale-[1.02]",
        link: "text-text-primary underline-offset-4 hover:underline hover:scale-[1.02]",
      },
      size: {
        default: "h-12 px-6 py-3",
        sm: "h-10 rounded-lg px-4 py-2",
        lg: "h-14 rounded-xl px-8 py-4",
        icon: "h-12 w-12",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button, buttonVariants }