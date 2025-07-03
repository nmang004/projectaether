import { ColumnDef } from "@tanstack/react-table"
import { Badge } from "@/components/ui/badge"

export interface AuditPage {
  url: string
  status_code: number
  response_time: number
  page_title: string
  meta_description: string
  h1_tags: string[]
  issues: string[]
}

const getStatusVariant = (status: number) => {
  if (status >= 200 && status < 300) return "default"
  if (status >= 300 && status < 400) return "secondary"
  if (status >= 400 && status < 500) return "destructive"
  if (status >= 500) return "destructive"
  return "outline"
}

const getIssueVariant = (issue: string) => {
  if (issue.includes("Error") || issue.includes("Missing")) return "destructive"
  if (issue.includes("Warning") || issue.includes("Long")) return "secondary"
  return "default"
}

export const columns: ColumnDef<AuditPage>[] = [
  {
    accessorKey: "url",
    header: "URL",
    cell: ({ row }) => (
      <div className="max-w-[300px] truncate">
        <a
          href={row.getValue("url")}
          target="_blank"
          rel="noopener noreferrer"
          className="text-blue-600 hover:underline"
        >
          {row.getValue("url")}
        </a>
      </div>
    ),
  },
  {
    accessorKey: "status_code",
    header: "Status",
    cell: ({ row }) => {
      const status = row.getValue("status_code") as number
      return (
        <Badge variant={getStatusVariant(status)}>
          {status}
        </Badge>
      )
    },
  },
  {
    accessorKey: "page_title",
    header: "Title",
    cell: ({ row }) => (
      <div className="max-w-[250px] truncate">
        {row.getValue("page_title") || "No title"}
      </div>
    ),
  },
  {
    accessorKey: "response_time",
    header: "Response Time",
    cell: ({ row }) => {
      const time = row.getValue("response_time") as number
      return <span>{time}ms</span>
    },
  },
  {
    accessorKey: "issues",
    header: "Issues",
    cell: ({ row }) => {
      const issues = row.getValue("issues") as string[]
      if (issues.length === 0) {
        return <Badge variant="default">No issues</Badge>
      }
      return (
        <div className="flex flex-wrap gap-1">
          {issues.slice(0, 3).map((issue, index) => (
            <Badge key={index} variant={getIssueVariant(issue)}>
              {issue}
            </Badge>
          ))}
          {issues.length > 3 && (
            <Badge variant="outline">+{issues.length - 3}</Badge>
          )}
        </div>
      )
    },
  },
]