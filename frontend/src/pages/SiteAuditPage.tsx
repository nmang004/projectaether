import { useState, useEffect } from "react"
import {
  getCoreRowModel,
  useReactTable,
  flexRender,
  getSortedRowModel,
  SortingState,
  getFilteredRowModel,
  ColumnFiltersState,
} from "@tanstack/react-table"
import { PageHeader } from "@/components/layout/PageHeader"
import { Progress } from "@/components/ui/progress"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { columns } from "./site-audit/columns"
import { useStartAudit, usePollAuditStatus } from "@/hooks/useSiteAudit"

export default function SiteAuditPage() {
  const [sorting, setSorting] = useState<SortingState>([])
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([])
  const [rootUrl, setRootUrl] = useState("")
  const [taskId, setTaskId] = useState<string | null>(null)
  
  const startAudit = useStartAudit()
  const auditStatus = usePollAuditStatus(taskId)
  
  const handleStartAudit = () => {
    if (!rootUrl.trim()) return
    
    startAudit.mutate(rootUrl, {
      onSuccess: (data) => {
        setTaskId(data.task_id)
      },
    })
  }
  
  const auditData = auditStatus.data?.result || []
  const progress = auditStatus.data?.progress || 0
  
  // Stop polling when audit is completed or failed
  useEffect(() => {
    if (auditStatus.data?.status === 'Completed' || auditStatus.data?.status === 'Failed') {
      // Query will automatically stop refetching when component unmounts or dependencies change
    }
  }, [auditStatus.data?.status])
  
  const table = useReactTable({
    data: auditData,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    state: {
      sorting,
      columnFilters,
    },
  })

  return (
    <div className="container mx-auto p-6">
      <PageHeader title="Live Site Audit Report" />
      
      <section className="mb-8">
        <div className="max-w-md space-y-4">
          <div className="space-y-2">
            <Label htmlFor="root-url">Root URL</Label>
            <Input
              id="root-url"
              value={rootUrl}
              onChange={(e) => setRootUrl(e.target.value)}
              placeholder="e.g., https://example.com"
              className="w-full"
            />
          </div>
          <Button 
            onClick={handleStartAudit}
            disabled={!rootUrl.trim() || startAudit.isPending}
            className="w-full"
          >
            {startAudit.isPending ? "Starting Audit..." : "Start Audit"}
          </Button>
        </div>
      </section>

      {startAudit.isError && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-md">
          <p className="text-red-700">
            Error starting audit: {startAudit.error?.message}
          </p>
        </div>
      )}

      {auditStatus.isError && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-md">
          <p className="text-red-700">
            Error getting audit status: {auditStatus.error?.message}
          </p>
        </div>
      )}

      {auditStatus.data?.status === 'Failed' && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-md">
          <p className="text-red-700">
            Audit failed: {auditStatus.data.error}
          </p>
        </div>
      )}

      {taskId && (
        <div className="mb-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-muted-foreground">
              {auditStatus.data?.status === 'Completed' ? 'Audit Complete' : 'Audit Progress'}
            </span>
            <span className="text-sm font-medium">{progress}%</span>
          </div>
          <Progress value={progress} className="w-full" />
          <p className="text-xs text-muted-foreground mt-1">
            Status: {auditStatus.data?.status || 'Starting...'}
          </p>
        </div>
      )}

      {auditStatus.data?.status === 'Completed' && auditData.length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <Input
              placeholder="Filter URLs..."
              value={(table.getColumn("url")?.getFilterValue() as string) ?? ""}
              onChange={(event) =>
                table.getColumn("url")?.setFilterValue(event.target.value)
              }
              className="max-w-sm"
            />
          </div>

          <div className="rounded-md border">
            <Table>
              <TableHeader>
                {table.getHeaderGroups().map((headerGroup) => (
                  <TableRow key={headerGroup.id}>
                    {headerGroup.headers.map((header) => (
                      <TableHead key={header.id}>
                        {header.isPlaceholder
                          ? null
                          : flexRender(
                              header.column.columnDef.header,
                              header.getContext()
                            )}
                      </TableHead>
                    ))}
                  </TableRow>
                ))}
              </TableHeader>
              <TableBody>
                {table.getRowModel().rows?.length ? (
                  table.getRowModel().rows.map((row) => (
                    <TableRow
                      key={row.id}
                      data-state={row.getIsSelected() && "selected"}
                    >
                      {row.getVisibleCells().map((cell) => (
                        <TableCell key={cell.id}>
                          {flexRender(cell.column.columnDef.cell, cell.getContext())}
                        </TableCell>
                      ))}
                    </TableRow>
                  ))
                ) : (
                  <TableRow>
                    <TableCell colSpan={columns.length} className="h-24 text-center">
                      No results.
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </div>

          <div className="flex items-center justify-between">
            <div className="text-sm text-muted-foreground">
              Showing {table.getRowModel().rows.length} of {auditData.length} pages
            </div>
          </div>
        </div>
      )}
    </div>
  )
}