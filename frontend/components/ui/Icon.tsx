import {
  Award,
  BookOpen,
  Building2,
  Cloud,
  CloudSun,
  Droplets,
  Flag,
  Globe2,
  GraduationCap,
  HandHeart,
  Handshake,
  Heart,
  Leaf,
  Lightbulb,
  Recycle,
  Scale,
  Search,
  ShieldCheck,
  Sprout,
  Target,
  TreePine,
  TrendingUp,
  Users,
  Waves,
  Wind,
  type LucideIcon,
} from "lucide-react";

/**
 * Icons editors can pick by name in the Django admin.
 *
 * Keeping this an explicit map means an unknown or mistyped name degrades to a
 * sensible default instead of crashing the page, and only these icons ship in
 * the bundle.
 */
const ICONS: Record<string, LucideIcon> = {
  award: Award,
  "book-open": BookOpen,
  building: Building2,
  cloud: Cloud,
  "cloud-sun": CloudSun,
  droplets: Droplets,
  flag: Flag,
  globe: Globe2,
  graduation: GraduationCap,
  "hand-heart": HandHeart,
  handshake: Handshake,
  heart: Heart,
  leaf: Leaf,
  lightbulb: Lightbulb,
  recycle: Recycle,
  scale: Scale,
  search: Search,
  "shield-check": ShieldCheck,
  sprout: Sprout,
  target: Target,
  tree: TreePine,
  "trending-up": TrendingUp,
  users: Users,
  waves: Waves,
  wind: Wind,
};

export function Icon({
  name,
  className,
}: {
  name: string;
  className?: string;
}) {
  const Component = ICONS[name?.toLowerCase()] ?? Leaf;
  return <Component className={className} aria-hidden />;
}

export const ICON_NAMES = Object.keys(ICONS);
