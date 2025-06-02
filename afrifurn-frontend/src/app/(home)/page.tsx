'use client'
import { Button } from "@/components/ui/button";
import { Carousel, CarouselContent, CarouselItem, CarouselPrevious, CarouselNext } from "@/components/ui/carousel";
import { AspectRatio } from "@radix-ui/react-aspect-ratio";
import Image from "next/image";
import Link from "next/link";

// Updated carousel items with Ikea-style messaging
const carouselItems = [
  {
    image: "/living.jpg",
    title: "Create a home that's you",
    description: "Affordable solutions for better living",
    link: "/rooms/living-room"
  },
  {
    image: "/f2.png",
    title: "Summer sale",
    description: "Up to 50% off selected items",
    link: "/offers"
  },
  {
    image: "/wide.png",
    title: "New lower price",
    description: "Making sustainable living more affordable",
    link: "/new-arrivals"
  }
]

// Room inspiration sections
const roomSections = [
  {
    title: "Living room",
    image: "/living.jpg",
    link: "/room/living-room",
    description: "Cozy solutions for your everyday space"
  },
  {
    title: "Bedroom",
    image: "/bedroom.jpg",
    link: "/room/bedroom",
    description: "For better sleep and peaceful mornings"
  },
  {
    title: "Kitchen",
    image: "/f2.png",
    link: "/room/kitchen",
    description: "The heart of the home"
  },
  {
    title: "Home office",
    image: "/office_1.png",
    link: "/room/office",
    description: "Functional workspaces for productivity"
  }
]

export default function HomePage() {
  return (
    // Wraap with Suspense
        <main className="max-w-[1920px] mx-auto bg-[#f5f5f5]">
      {/* Hero Carousel */}
      <section className="relative h-[70vh] md:h-[65vh]">
        <Carousel className="w-full h-full">
          <CarouselContent className="h-full">
            {carouselItems.map((item, index) => (
              <CarouselItem key={index} className="h-full">
                <div className="relative h-[70vh]">
                  <AspectRatio ratio={16/9} className="hidden md:block h-[70vh]">
                    <Image
                      src={item.image}
                      alt={item.title}
                      fill
                      className="object-cover"
                      priority
                      sizes="(max-width: 768px) 100vw, 100vw"
                      quality={100}
                    />
                  </AspectRatio>
                  {/* Mobile-specific image container */}
                  <div className="block md:hidden h-full">
                   <AspectRatio className="h-full"></AspectRatio>
                    <Image
                      src={item.image}
                      alt={item.title}
                      fill
                      className="object-cover"
                      priority
                    />
                  </div>
                  <div className="absolute inset-0 flex items-center justify-start bg-black/10">
                    <div className="text-left text-black max-w-md px-6 md:px-12 py-6 bg-white/60 ml-0 md:ml-16 transform transition-all duration-700">
                      <h2 className="text-xl md:text-3xl font-bold mb-2 md:mb-3">{item.title}</h2>
                      <p className="text-sm md:text-lg mb-3 md:mb-4">{item.description}</p>
                      <Link href={item.link}>
                        <Button className="bg-[#0058a3] hover:bg-[#004f93] text-white rounded-none px-4 py-2 text-sm font-medium">
                          Shop now
                        </Button>
                      </Link>
                    </div>
                  </div>
                </div>
              </CarouselItem>
            ))}
          </CarouselContent>
          <CarouselPrevious className="left-2 md:left-8 h-8 w-8 md:h-10 md:w-10 bg-white text-black border-none rounded-full" />
          <CarouselNext className="right-2 md:right-8 h-8 w-8 md:h-10 md:w-10 bg-white text-black border-none rounded-full" />
        </Carousel>
      </section>

      {/* Popular categories */}
      {/* <section className="py-12 px-4 md:px-8">
        <h2 className="text-2xl md:text-3xl font-bold mb-8 text-center">Popular categories</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-8">
          {['Tv Stands', 'Bedsides', 'Tables', 'Storage', 'Lighting', 'Textiles', 'Decoration', 'Kitchenware'].map((category, index) => (
            <Link href={`/room/${category.toLowerCase()}`} key={index}>
              <div className="bg-white p-4 text-center hover:shadow-md transition-shadow duration-300">
                <div className="w-16 h-16 md:w-24 md:h-24 bg-[#f5f5f5] rounded-full mx-auto mb-4 flex items-center justify-center">
                  <span className="text-2xl">🪑</span>
                </div>
                <p className="font-medium">{category}</p>
              </div>
            </Link>
          ))}
        </div>
      </section> */}

      {/* Room inspiration */}
      <section className="py-8 px-4 md:px-8">
        <h2 className="text-2xl md:text-3xl font-bold mb-8 text-center">Room inspiration</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {roomSections.map((room, index) => (
            <div key={index} className="bg-white group overflow-hidden">
              <div className="relative aspect-[4/3]">
                <Image
                  src={room.image}
                  alt={room.title}
                  fill
                  className="object-cover transition-transform duration-500 group-hover:scale-105"
                />
              </div>
              <div className="p-6">
                <h3 className="text-xl md:text-2xl font-bold mb-2">{room.title}</h3>
                <p className="text-gray-600 mb-4">{room.description}</p>
                <Link href={room.link}>
                  <Button className="bg-[#0058a3] hover:bg-[#004f93] text-white rounded-none px-6 py-2 text-sm font-medium">
                    Shop {room.title.toLowerCase()}
                  </Button>
                </Link>
              </div>
            </div>
          ))}
        </div>
      </section>

    

      {/* Sustainability section */}
      <section className="py-12 px-4 md:px-8 bg-white my-8">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-2xl md:text-3xl font-bold mb-4">Sustainable living</h2>
          <p className="text-lg mb-8">We're committed to creating a better everyday life while protecting our planet.</p>
          <Link href="/sustainability">
            <Button className="bg-transparent border-2 border-[#0058a3] text-[#0058a3] hover:bg-[#0058a3] hover:text-white rounded-none px-8 py-3 text-base font-medium transition-colors duration-300">
              Learn more about our initiatives
            </Button>
          </Link>
        </div>
      </section>
    </main>
  
  );
}