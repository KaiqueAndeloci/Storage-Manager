"use client"
import { Button } from '@/components/ui/button';
import { Spinner } from '@/components/ui/spinner';
import { useFormStatus } from "react-dom";
import { cn } from "@/lib/utils"


export function ButtonSubmit({ text, className, size }: { text?: string, className?: string, size?: "default" | "sm" | "lg" | "icon" | "xl" | null }) {
    const { pending } = useFormStatus()
    return (
        <Button size={size} className={className} disabled={pending} type='submit'>
            <Spinner className={cn(!pending && 'hidden')}></Spinner>
            {text ? text : 'Send'}
        </Button>
    )
}
