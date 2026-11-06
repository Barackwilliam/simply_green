/** Shapes returned by the Django REST API. Keep in step with the serializers. */

export interface Paginated<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface SocialLink {
  platform: string;
  label: string;
  url: string;
}

export interface SiteSettings {
  organisation_name: string;
  acronym: string;
  tagline: string;
  logo: string | null;
  logo_light: string | null;
  favicon: string | null;
  registration_number: string;
  registration_statement: string;
  vision: string;
  mission: string;
  who_we_are: string;
  email: string;
  secondary_email: string;
  phone: string;
  secondary_phone: string;
  whatsapp: string;
  address: string;
  postal_address: string;
  city: string;
  country: string;
  map_embed_url: string;
  latitude: string | null;
  longitude: string | null;
  default_meta_title: string;
  default_meta_description: string;
  default_og_image: string | null;
  google_analytics_id: string;
  google_site_verification: string;
  donate_enabled: boolean;
  volunteer_enabled: boolean;
  newsletter_enabled: boolean;
  social_links: SocialLink[];
}

export interface Partner {
  id: number;
  name: string;
  slug: string;
  kind: string;
  kind_label: string;
  logo: string | null;
  website: string;
  description: string;
  is_featured: boolean;
}

export interface ImpactStat {
  id: number;
  label: string;
  value: string;
  suffix: string;
  icon: string;
  description: string;
}

export interface CoreValue {
  id: number;
  title: string;
  description: string;
  icon: string;
}

export interface Objective {
  id: number;
  text: string;
}

export interface PartnerReason {
  id: number;
  title: string;
  description: string;
  icon: string;
}

export interface TeamMember {
  id: number;
  full_name: string;
  slug: string;
  role: string;
  group: string;
  group_label: string;
  photo: string | null;
  short_bio: string;
  bio: string;
  email: string;
  linkedin: string;
  x_handle: string;
}

export interface FocusArea {
  id: number;
  title: string;
  slug: string;
  summary: string;
  icon: string;
  image: string | null;
  accent_colour: string;
  body?: string;
  meta_title?: string;
  meta_description?: string;
  og_image?: string | null;
  noindex?: boolean;
}

export interface ProgrammeOutcome {
  id: number;
  label: string;
  value: string;
}

export interface ProgrammeImage {
  id: number;
  image: string;
  caption: string;
  alt_text: string;
}

export interface Programme {
  id: number;
  title: string;
  slug: string;
  subtitle: string;
  status: string;
  status_label: string;
  summary: string;
  featured_image: string | null;
  location: string;
  region: string;
  district: string;
  beneficiaries: string;
  beneficiary_count: number | null;
  start_date: string | null;
  end_date: string | null;
  focus_areas: FocusArea[];
  is_featured: boolean;
  body?: string;
  outcomes?: ProgrammeOutcome[];
  images?: ProgrammeImage[];
  partners?: Partner[];
  meta_title?: string;
  meta_description?: string;
  og_image?: string | null;
  noindex?: boolean;
}

export interface Publication {
  id: number;
  title: string;
  slug: string;
  kind: string;
  kind_label: string;
  summary: string;
  download_url: string;
  cover_image: string | null;
  published_date: string | null;
  year: number | null;
  page_count: number | null;
  file_size_label: string;
  programme: number | null;
  programme_title: string;
  is_featured: boolean;
  download_count: number;
}

export interface Category {
  id: number;
  name: string;
  slug: string;
  description: string;
  colour: string;
}

export interface Post {
  id: number;
  kind: string;
  kind_label: string;
  title: string;
  slug: string;
  excerpt: string;
  featured_image: string | null;
  featured_image_alt: string;
  category: Category | null;
  tags: string[];
  author_display: string;
  published_at: string;
  reading_minutes: number | null;
  is_featured: boolean;
  body?: string;
  featured_image_credit?: string;
  audio_url?: string;
  audio_file?: string | null;
  programme_title?: string;
  programme_slug?: string;
  view_count?: number;
  meta_title?: string;
  meta_description?: string;
  og_image?: string | null;
  noindex?: boolean;
}

export interface SiteEvent {
  id: number;
  title: string;
  slug: string;
  summary: string;
  featured_image: string | null;
  start_datetime: string;
  end_datetime: string | null;
  status: string;
  status_label: string;
  venue: string;
  is_online: boolean;
  registration_enabled: boolean;
  registration_open: boolean;
  is_featured: boolean;
  body?: string;
  address?: string;
  map_embed_url?: string;
  online_url?: string;
  registration_deadline?: string | null;
  capacity?: number | null;
  meta_title?: string;
  meta_description?: string;
  og_image?: string | null;
  noindex?: boolean;
}

export interface Photo {
  id: number;
  image: string;
  caption: string;
  alt_text: string;
  credit: string;
}

export interface Album {
  id: number;
  title: string;
  slug: string;
  description: string;
  cover_image: string | null;
  date: string | null;
  location: string;
  photo_count: number;
  is_featured: boolean;
  photos?: Photo[];
}

export interface Video {
  id: number;
  title: string;
  slug: string;
  description: string;
  source: string;
  source_label: string;
  video_url: string;
  video_file: string | null;
  thumbnail: string | null;
  duration_label: string;
  date: string | null;
  is_featured: boolean;
}

export interface DonationMethod {
  id: number;
  channel: string;
  channel_label: string;
  label: string;
  account_name: string;
  account_number: string;
  bank_name: string;
  branch: string;
  swift_code: string;
  currency: string;
  instructions: string;
  icon: string | null;
}
