import { Button } from "@/components/ui/button"
import { SiteHeader } from "@/components/site-header"
import { FeatureCard } from "@/components/feature-card"
import { FAQItem } from "@/components/faq-item"
import { PricingCard } from "@/components/pricing-card"

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col">
      <SiteHeader />
      <main className="flex-1">
        {/* Hero section */}
        <section className="space-y-6 pb-8 pt-6 md:pb-12 md:pt-10 lg:py-32">
          <div className="container flex max-w-[64rem] flex-col items-center gap-4 text-center mx-auto">
            <h1 className="font-heading text-3xl sm:text-5xl md:text-6xl lg:text-7xl">
              Organize Your Tasks with{" "}
              <span className="text-primary">TersuTodo</span>
            </h1>
            <p className="max-w-[42rem] leading-normal text-muted-foreground sm:text-xl sm:leading-8">
              Boost your productivity with our intuitive Kanban-style todo
              application. Manage tasks efficiently with multiple views, priorities,
              and more.
            </p>
            <div className="space-x-4">
              <Button size="lg" asChild>
                <a href="/auth/register">Get Started</a>
              </Button>
              <Button size="lg" variant="outline">
                Learn More
              </Button>
            </div>
          </div>
        </section>

        {/* Features section */}
        <section className="container space-y-6 py-8 md:py-12 lg:py-24 mx-auto">
          <div className="mx-auto flex max-w-[58rem] flex-col items-center space-y-4 text-center">
            <h2 className="font-heading text-3xl leading-[1.1] sm:text-3xl md:text-6xl">
              Features
            </h2>
            <p className="max-w-[85%] leading-normal text-muted-foreground sm:text-lg sm:leading-7">
              Everything you need to manage your tasks effectively
            </p>
          </div>
          <div className="mx-auto grid justify-center gap-4 sm:grid-cols-2 md:max-w-[64rem] md:grid-cols-3">
            <FeatureCard
              icon="ListTodo"
              title="List View"
              description="Traditional list view with checkboxes and quick actions"
            />
            <FeatureCard
              icon="Grid"
              title="Grid View"
              description="Visual grid layout with priority-based coloring"
            />
            <FeatureCard
              icon="Kanban"
              title="Kanban Board"
              description="Drag-and-drop interface for visual task management"
            />
          </div>
        </section>

        {/* FAQ section */}
        <section className="container py-8 md:py-12 lg:py-24 mx-auto">
          <div className="mx-auto max-w-[58rem] space-y-6">
            <h2 className="font-heading text-3xl leading-[1.1] sm:text-3xl md:text-6xl text-center">
              FAQ
            </h2>
            <div className="space-y-4">
              <FAQItem
                question="Is TersuTodo free to use?"
                answer="Yes, TersuTodo offers a generous free tier with all essential features. Premium features are available for power users."
              />
              <FAQItem
                question="Can I collaborate with my team?"
                answer="Yes, TersuTodo supports team collaboration with shared boards and real-time updates."
              />
              <FAQItem
                question="How secure is my data?"
                answer="We use industry-standard encryption and security practices to protect your data."
              />
            </div>
          </div>
        </section>

        {/* Pricing section */}
        <section className="container py-8 md:py-12 lg:py-24 mx-auto">
          <div className="mx-auto max-w-[58rem] space-y-6">
            <h2 className="font-heading text-3xl leading-[1.1] sm:text-3xl md:text-6xl text-center">
              Pricing
            </h2>
            <div className="grid gap-6 sm:grid-cols-2">
              <PricingCard
                title="Free"
                price="$0"
                description="For individuals and small teams"
                features={[
                  "Unlimited tasks",
                  "3 project boards",
                  "Basic prioritization",
                  "7-day history"
                ]}
              />
              <PricingCard
                title="Pro"
                price="$9.99"
                description="For power users and large teams"
                features={[
                  "Everything in Free",
                  "Unlimited project boards",
                  "Advanced prioritization",
                  "Unlimited history",
                  "Team collaboration"
                ]}
              />
            </div>
          </div>
        </section>
      </main>
      <footer className="border-t py-6 md:py-0">
        <div className="container flex flex-col items-center justify-between gap-4 md:h-24 md:flex-row mx-auto">
          <p className="text-center text-sm leading-loose text-muted-foreground md:text-left">
            Built by{" "}
            <a href="#" className="font-medium underline underline-offset-4">
              TersuTodo
            </a>
            . The source code is available on{" "}
            <a
              href="#"
              className="font-medium underline underline-offset-4"
            >
              GitHub
            </a>
            .
          </p>
        </div>
      </footer>
    </div>
  )
}

