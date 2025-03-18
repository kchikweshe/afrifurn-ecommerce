'use client'

import React, { useState, useEffect } from 'react'
import Image from 'next/image'
import Link from 'next/link'
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Carousel, CarouselContent, CarouselItem, CarouselNext, CarouselPrevious } from "@/components/ui/carousel"

export interface Slide {
  image: string
  title: string
  description: string
  link: string
}

interface ImageCarouselProps {
  carouselSlides: Slide[]
}

export function ImageCarousel({ carouselSlides }: ImageCarouselProps) {
  const [currentIndex, setCurrentIndex] = useState(0)

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentIndex((prevIndex) => (prevIndex + 1) % carouselSlides.length)
    }, 5000)
    return () => clearInterval(timer)
  }, [carouselSlides.length])

  return (
    <Carousel className="w-full max-w-6xl mx-auto relative">
      <CarouselContent>
        {carouselSlides.map((slide, index) => (
          <CarouselItem key={index} className="relative">
            <Card className="border-none">
              <CardContent className="p-0 aspect-[16/9] overflow-hidden">
                <Image
                  src={slide.image}
                  alt={slide.title}
                  width={1200}
                  height={675}
                  className="object-cover w-full h-full"
                  priority={index === 0}
                />
                <div className="absolute inset-0 bg-gradient-to-r from-black/60 to-transparent" />
                <div className="absolute inset-0 flex flex-col justify-center p-8 text-white">
                  <h2 className="text-2xl md:text-4xl font-bold mb-2 md:mb-4">{slide.title}</h2>
                  <p className="text-sm md:text-lg mb-4 md:mb-6 max-w-md">{slide.description}</p>
                  <Button asChild className="w-fit" variant="secondary">
                    <Link href={slide.link}>Shop Now</Link>
                  </Button>
                </div>
              </CardContent>
            </Card>
          </CarouselItem>
        ))}
      </CarouselContent>
      <div className="absolute bottom-4 left-0 right-0 flex justify-center space-x-2">
        {carouselSlides.map((_, index) => (
          <button
            key={index}
            className={`h-2 w-2 rounded-full transition-all duration-300 ${
              index === currentIndex ? 'bg-white w-4' : 'bg-white/50 hover:bg-white/75'
            }`}
            onClick={() => setCurrentIndex(index)}
            aria-label={`Go to slide ${index + 1}`}
          />
        ))}
      </div>
      <CarouselPrevious className="absolute left-4 top-1/2 -translate-y-1/2" />
      <CarouselNext className="absolute right-4 top-1/2 -translate-y-1/2" />
    </Carousel>
  )
}