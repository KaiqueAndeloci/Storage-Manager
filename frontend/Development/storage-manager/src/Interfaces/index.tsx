export type message_type = 'ERROR' | 'SUCCESS'

export type permission_type = 'ADMIN' | 'cashier' | 'logistic'

export interface chart_data_interface {
    date: string,
    desktop: number,
    mobile: number
}

export interface user {
    name: string,
    email: string,
    permission_type: permission_type,
    date_creation: string
}

export interface page_auth {
    page_name: string
}

export interface AuthenticateContext {
    user_credentials?: user,
    page_details?: page_auth,
    login: (
        name: string,
        email: string,
        userPermission: permission_type
    ) => void,
    logout: () => void,
    // notify: ({ message, message_type }: { message: string, message_type: message_type }) => void,
}


export type formResponse = { success: true, response_api: any } | { success: false, response_api: any };
