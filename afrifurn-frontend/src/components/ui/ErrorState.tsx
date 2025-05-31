'use client'
import React from 'react'

// Error component following Single Responsibility Principle
const ErrorState = ({ message }: { message: string }) => (
    <div className="container mx-auto px-4 py-8">Error: {message}</div>
)

export default ErrorState 