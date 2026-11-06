/** The site's primary navigation, mirroring the client's content structure. */

export interface NavChild {
  label: string;
  href: string;
  description?: string;
}

export interface NavItem {
  label: string;
  href: string;
  children?: NavChild[];
}

export const NAV_ITEMS: NavItem[] = [
  { label: "Home", href: "/" },
  {
    label: "About Us",
    href: "/about",
    children: [
      { label: "Who We Are", href: "/about", description: "Our story and registration" },
      { label: "Vision & Mission", href: "/about#vision", description: "What we are working towards" },
      { label: "Core Values", href: "/about#values", description: "The principles that guide us" },
      { label: "Our Objectives", href: "/about#objectives", description: "What we set out to achieve" },
      { label: "Our Team", href: "/about/team", description: "The people behind the work" },
    ],
  },
  {
    label: "Focus Areas",
    href: "/focus-areas",
    children: [
      { label: "All Focus Areas", href: "/focus-areas", description: "The seven themes we work across" },
    ],
  },
  {
    label: "Programmes",
    href: "/programmes",
    children: [
      { label: "All Programmes", href: "/programmes", description: "Everything we are running" },
      { label: "Current Programmes", href: "/programmes?status=ongoing", description: "Active in the field today" },
      { label: "Completed Projects", href: "/programmes?status=completed", description: "Work we have delivered" },
    ],
  },
  {
    label: "Resources",
    href: "/resources",
    children: [
      { label: "All Publications", href: "/resources", description: "Reports, research and briefs" },
      { label: "Annual Reports", href: "/resources?kind=annual_report" },
      { label: "Impact Reports", href: "/resources?kind=impact_report" },
      { label: "Research", href: "/resources?kind=research" },
    ],
  },
  {
    label: "News & Events",
    href: "/news",
    children: [
      { label: "News", href: "/news", description: "Latest from our work" },
      { label: "Events", href: "/events", description: "What is coming up" },
      { label: "Announcements", href: "/news?kind=announcement" },
      { label: "Impact Stories", href: "/news?kind=impact_story" },
      { label: "Podcasts", href: "/news?kind=podcast" },
    ],
  },
  {
    label: "Gallery",
    href: "/gallery",
    children: [
      { label: "Photos", href: "/gallery", description: "Albums from our activities" },
      { label: "Videos", href: "/gallery/videos", description: "Film from the field" },
    ],
  },
  {
    label: "Get Involved",
    href: "/get-involved",
    children: [
      { label: "Become a Volunteer", href: "/get-involved/volunteer", description: "Give your time and skills" },
      { label: "Partner With Us", href: "/get-involved/partner", description: "Work alongside us" },
      { label: "Support Our Work", href: "/donate", description: "Fund community-led action" },
    ],
  },
  { label: "Contact", href: "/contact" },
];
