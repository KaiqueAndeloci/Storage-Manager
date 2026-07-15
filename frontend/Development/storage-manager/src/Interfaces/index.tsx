export type message_type = 'ERROR' | 'SUCCESS'

export type permission_type = 'ADMIN' | 'cashier' | 'logistic'

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


export type formResponse = { success: true, response_api: any } | { success: false, response_api: any };
