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
    title: "Office",
    image: "/office_1.png",
    link: "/room/office",
    description: "Functional workspaces for productivity"
  }
]


const textOverlay = (title: string, description: string, link: string) => <div className="absolute inset-0 flex items-center justify-start bg-black/10">
  <div className="text-left text-black max-w-md px-6 md:px-12 py-6 bg-white/60 ml-0 md:ml-16 transform transition-all duration-700">
    <h2 className="text-xl md:text-3xl font-bold mb-2 md:mb-3">{title}</h2>
    <p className="text-sm md:text-lg mb-3 md:mb-4">{description}</p>
    <Link href={link}>
      <Button className="bg-[#0058a3] hover:bg-[#004f93] text-white rounded-none px-4 py-2 text-sm font-medium">
        Shop now
      </Button>
    </Link>
  </div>
</div>

export default function HomePage() {
  return (
    // Wraap with Suspense
    <main >
      {/* Hero Carousel */}
      <section className="w-full relative h-[70vh] md:h-[65vh]">
        <Carousel>
          <CarouselContent className="h-full">
            {carouselItems.map((item, index) => (
              <CarouselItem key={index} className="h-full">
                <div className="relative h-[70vh]">
                  <AspectRatio ratio={16 / 9} className="hidden md:block h-[70vh]">
                    <Image
                      src={item.image}
                      alt={item.title}
                      fill
                      className="object-cover"
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


      {/* Room inspiration */}
      <section className="py-8 mx-2 ">
        <h2 className="text-2xl md:text-3xl font-bold mb-4 text-center p-3 text-blue-600">Room Inspiration</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {roomSections.map((room, index) => (
            <Link href={room.link}>
              <div key={index} className="relative rounded-xl overflow-hidden group">
                {/* Image */}

                <div className="relative aspect-[4/3]">
                  <Image
                    src={room.image}
                    alt={room.title}
                    fill
                    className="object-cover rounded-xl transition-transform duration-500 group-hover:scale-105"
                  />
                </div>

                {/* Text Overlay */}
                <div className="absolute inset-0 bg-black/40 text-white p-6 flex flex-col justify-end z-10">
                  <h3 className="text-xl md:text-2xl font-bold mb-2">{room.title}</h3>
                  <p className="mb-4">{room.description}</p>

                </div>
              </div></Link>

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