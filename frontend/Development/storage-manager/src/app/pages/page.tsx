'use server'
import Link from "next/link";
import {
    ArrowUpRight,
} from "lucide-react";
import { PageItem } from "@/Interfaces/index"
import { routes_deitails } from '@/app/routes'


export default async function Pages() {
    const list_pages: PageItem[] = routes_deitails;
    return (
        <main className="mx-auto w-full max-w-7xl p-6 md:p-10">
            <header className="mb-8">
                <h1 className="text-3xl font-bold tracking-tight">
                    Páginas do sistema
                </h1>
                <p className="mt-2 text-muted-foreground">
                    Selecione uma página para acessar suas funcionalidades.
                </p>
            </header>

            <section className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                {list_pages.map((page) => {
                    const Icon = page.icon;

                    return (
                        <Link
                            key={page.href}
                            href={page.href}
                            className="group rounded-xl border bg-card p-5 transition-all duration-200 hover:-translate-y-1 hover:border-primary/50 hover:shadow-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                        >
                            <div className="mb-5 flex items-center justify-between">
                                <div className="flex size-11 items-center justify-center rounded-lg bg-primary/10 text-primary">
                                    <Icon className="size-6" />
                                </div>

                                <ArrowUpRight className="size-5 text-muted-foreground transition-transform group-hover:-translate-y-1 group-hover:translate-x-1" />
                            </div>

                            <h2 className="text-lg font-semibold">
                                {page.title}
                            </h2>

                            <p className="mt-2 text-sm leading-6 text-muted-foreground">
                                {page.description}
                            </p>
                        </Link>
                    );
                })}
            </section>
        </main>
    );
}
