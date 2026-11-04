import {
    LayoutDashboard,
    Package,
    Users,
    ShieldCheck,
    Settings,
} from "lucide-react";
import { PageItem } from '@/Interfaces/index'

export const routes = {
    home: '/',
    login: '/login',
    pages: '/pages',
    storages: '/pages/storages',
    dashboard: '/pages/dashboard',
    management: '/pages/management',
    managementPermissions: '/pages/management/permissions',
    products: '/pages/products',
    configuration: '/pages/config'
};

export const routes_deitails: PageItem[] = [
    {
        title: "Usuários",
        description: "Consulte e gerencie os usuários.",
        href: routes.management,
        icon: Users,
    },
    {
        title: "Dashboard",
        description: "Visualize as informações gerais do sistema.",
        href: routes.dashboard,
        icon: LayoutDashboard,
    },
    {
        title: "Produtos",
        description: "Consulte e organize seus produtos.",
        href: routes.products,
        icon: Package,
    },
    {
        title: "Permissões",
        description: "Gerencie as permissões de acesso.",
        href: routes.managementPermissions,
        icon: ShieldCheck,
    },
    {
        title: "Configurações",
        description: "Configure as opções do sistema.",
        href: routes.configuration,
        icon: Settings,
    },
]
