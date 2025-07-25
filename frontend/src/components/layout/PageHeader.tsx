interface PageHeaderProps {
  title: string;
}

export function PageHeader({ title }: PageHeaderProps) {
  return (
    <h1 className="text-3xl font-bold tracking-tight mb-6">
      {title}
    </h1>
  );
}