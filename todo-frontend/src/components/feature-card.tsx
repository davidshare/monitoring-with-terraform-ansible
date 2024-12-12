import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ListTodo, Grid, Kanban } from 'lucide-react'

const iconMap = {
  ListTodo,
  Grid,
  Kanban,
}

interface FeatureCardProps {
  icon: keyof typeof iconMap
  title: string
  description: string
}

export function FeatureCard({ icon, title, description }: FeatureCardProps) {
  const Icon = iconMap[icon]

  return (
    <Card>
      <CardHeader>
        <Icon className="h-14 w-14 text-primary" />
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-muted-foreground">{description}</p>
      </CardContent>
    </Card>
  )
}

