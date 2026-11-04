"use client"
import { Button } from '@/components/ui/button';
import { Spinner } from '@/components/ui/spinner';
import { useFormStatus } from "react-dom";
import { cn } from "@/lib/utils"


export function ButtonSubmit({ text, className, size, handleOnClick, disabled }: {
    text?: string,
    className?: string,
    size?: "default" | "sm" | "lg" | "icon" | "xs" | "icon-xs" | "icon-sm" | "icon-lg" | null | undefined,
    handleOnClick?: () => void,
    disabled?: boolean
}) {
    const { pending } = useFormStatus()
    return (
        <Button size={size} className={className} disabled={pending || disabled} type='submit' onClick={handleOnClick}>
            <Spinner className={cn(!pending && 'hidden')}></Spinner>
            {text ? text : 'Send'}
        </Button>
    )
}
