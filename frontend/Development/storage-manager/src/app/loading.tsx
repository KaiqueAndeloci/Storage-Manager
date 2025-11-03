export default function Loading() {
    return (
        <div className="w-full h-full fixed bg-black opacity-50 top-0 right-0">
            <div className="flex items-center justify-center h-full w-full">
                <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
            </div>
        </div>
    )
}