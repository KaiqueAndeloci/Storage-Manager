export type message_type = 'ERROR' | 'SUCCESS'
import {
    type LucideIcon,
} from "lucide-react";
export type permission_type = 'ADMIN' | 'cashier' | 'logistic'

export type PageItem = {
    title: string;
    description: string;
    href: string;
    icon: LucideIcon;
};

export interface chart_data_interface {
    "ID": number,
    "Name": string,
    "Details": string,
    "ID_image": number,
    "ID_storage": number,
    "value": number,
    "Token_product": string,
    "Category": string,
    "State": string
}

export interface chart_data_interface2 {
    date: string,
    desktop: number,
    mobile: number
}

export interface user {
    name: string
}

export interface page {
    name: string,
    Limit: number,
    Offset: number,
    Total: number
}

export interface AuthenticateContext {
    user_details?: user,
    page?: page,
    setPage: (page: page) => void,
    logout: () => void,
    // notify: ({ message, message_type }: { message: string, message_type: message_type }) => void,
}

export interface Users {
    ID: number;
    Name: string;
    DateCreation: string;
    UserType: string;
}

export interface Users_table extends Users {
    checked: boolean
}

export interface Edit_User extends Users_table {
    email?: string;
    Phone_Number?: number;
    DDD_Number?: number;
    Work_Position?: string;
    Leader_Email?: string;
}

export type formResponse = { success: true, response_api: any } | { success: false, response_api: any };

export type fieldType =
    "button"
    | "checkbox"
    | "color"
    | "date"
    | "datetime-local"
    | "email"
    | "file"
    | "hidden"
    | "image"
    | "month"
    | "number"
    | "password"
    | "radio"
    | "range"
    | "reset"
    | "search"
    | "submit"
    | "tel"
    | "text"
    | "time"
    | "url"
    | "week"
    | "dual-listbox"

export type transferItem = {
    id: string
    label: string
}

export type transferListProps = {
    available: transferItem[]
    selected: transferItem[]
    // onChange: (next: { available: TransferItem[]; selected: TransferItem[] }) => void
}
export interface fieldModel {
    name: string,
    placeholder: string,
    className: string,
    type: fieldType,
    hidden: boolean,
    maxLength: number,
    transferListProps?: transferListProps,
    defaultValue?: string | number,
    label?: string[],
    setRadioState?: (value: string) => void,
    radioState?: string
}