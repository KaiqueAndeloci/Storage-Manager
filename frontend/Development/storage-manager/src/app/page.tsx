'use server'

import { ButtonSubmit } from "@/components/custom/button";
import { routes } from "@/app/routes";
import {
    Boxes,
    LayoutDashboard,
    Settings2,
    ArrowUpRight,
} from "lucide-react";

const features = [
    {
        title: "Organization",
        description: "Navigation separated by cards and different views of your containers.",
        icon: Boxes,
    },
    {
        title: "Dashboard",
        description: "Get a clear overview of your products and important information.",
        icon: LayoutDashboard,
    },
    {
        title: "Management",
        description: "Manage your products with a simple and organized interface.",
        icon: Settings2,
    },
];

export default async function Home() {
    return (
        <main className="mx-auto flex w-full max-w-6xl flex-col items-center gap-12 px-6 py-16 text-white">
            <section className="flex w-full max-w-4xl flex-col items-center gap-6 text-center">
                <h1 className="text-4xl font-extrabold tracking-tight text-balance sm:text-5xl md:text-7xl">
                    The everything app, for storage manager
                </h1>

                <p className="max-w-2xl text-base text-gray-300 sm:text-lg">
                    One app for professional projects, organization,
                    maximum time-efficiency and more.
                </p>

                <a href={routes.login}>
                    <ButtonSubmit
                        size={null}
                        className="h-15 rounded-md px-10 text-lg hover:cursor-pointer"
                        text="Get started"
                    />
                </a>
            </section>

            <section className="w-full space-y-6">
                <div className="text-center">
                    <h2 className="text-2xl font-bold sm:text-3xl">
                        Maximize your work efficiency
                    </h2>
                    <p className="mt-2 text-sm text-gray-400">
                        Everything you need in one place.
                    </p>
                </div>

                <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
                    {features.map((feature) => {
                        const Icon = feature.icon;

                        return (
                            <article
                                key={feature.title}
                                className="group flex min-h-56 flex-col rounded-xl border border-white/10 bg-white/5 p-6 transition-all duration-200 hover:-translate-y-1 hover:border-white/20 hover:bg-white/10"
                            >
                                <div className="mb-5 flex size-12 items-center justify-center rounded-lg bg-white/10">
                                    <Icon className="size-6" />
                                </div>

                                <h3 className="text-lg font-semibold">
                                    {feature.title}
                                </h3>

                                <p className="mt-2 flex-1 text-sm leading-6 text-gray-400">
                                    {feature.description}
                                </p>

                                <div className="mt-4 flex justify-end">
                                    <ArrowUpRight className="size-5 text-gray-400 transition-transform group-hover:translate-x-1 group-hover:-translate-y-1" />
                                </div>
                            </article>
                        );
                    })}
                </div>
            </section>
        </main>
    );
}
