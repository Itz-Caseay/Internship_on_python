#!/usr/bin/env python3
"""
Map Tracker - A comprehensive GPS tracking and location management application
Features: Real-time tracking, location history, route planning, POI management
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkinter import font as tkfont
import json
import os
import math
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import threading
import time
import webbrowser

# ============================================================================
# DATA LAYER
# ============================================================================

class Location:
    """Location model representing a geographical point"""
    
    def __init__(self, 
                 name: str,
                 latitude: float,
                 longitude: float,
                 address: str = "",
                 description: str = "",
                 category: str = "General",
                 is_favorite: bool = False):
        
        self.id = self._generate_id()
        self.name = name.strip()
        self.latitude = latitude
        self.longitude = longitude
        self.address = address.strip()
        self.description = description.strip()
        self.category = category
        self.is_favorite = is_favorite
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.visit_count = 0
        self.last_visited = None
        self.tags = []
    
    def _generate_id(self) -> str:
        """Generate a unique ID"""
        return f"LOC{datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(100, 999)}"
    
    def calculate_distance(self, other_lat: float, other_lon: float) -> float:
        """Calculate distance to another point using Haversine formula"""
        R = 6371  # Earth's radius in kilometers
        
        lat1, lon1 = math.radians(self.latitude), math.radians(self.longitude)
        lat2, lon2 = math.radians(other_lat), math.radians(other_lon)
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c  # Distance in kilometers
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'address': self.address,
            'description': self.description,
            'category': self.category,
            'is_favorite': self.is_favorite,
            'visit_count': self.visit_count,
            'last_visited': self.last_visited.isoformat() if self.last_visited else None,
            'tags': self.tags,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Location':
        """Create from dictionary"""
        loc = cls(
            name=data['name'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            address=data.get('address', ''),
            description=data.get('description', ''),
            category=data.get('category', 'General'),
            is_favorite=data.get('is_favorite', False)
        )
        loc.id = data['id']
        loc.visit_count = data.get('visit_count', 0)
        loc.tags = data.get('tags', [])
        loc.created_at = datetime.fromisoformat(data['created_at'])
        loc.updated_at = datetime.fromisoformat(data['updated_at'])
        if data.get('last_visited'):
            loc.last_visited = datetime.fromisoformat(data['last_visited'])
        return loc

class TrackPoint:
    """Track point for GPS tracking"""
    
    def __init__(self, latitude: float, longitude: float, speed: float = 0, altitude: float = 0):
        self.id = self._generate_id()
        self.latitude = latitude
        self.longitude = longitude
        self.speed = speed
        self.altitude = altitude
        self.timestamp = datetime.now()
        self.accuracy = 0
    
    def _generate_id(self) -> str:
        return f"TP{datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(100, 999)}"
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            'id': self.id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'speed': self.speed,
            'altitude': self.altitude,
            'timestamp': self.timestamp.isoformat(),
            'accuracy': self.accuracy
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'TrackPoint':
        tp = cls(data['latitude'], data['longitude'], data['speed'], data['altitude'])
        tp.id = data['id']
        tp.timestamp = datetime.fromisoformat(data['timestamp'])
        tp.accuracy = data.get('accuracy', 0)
        return tp

class Route:
    """Route consisting of multiple track points"""
    
    def __init__(self, name: str, description: str = ""):
        self.id = self._generate_id()
        self.name = name.strip()
        self.description = description.strip()
        self.points = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.distance = 0
        self.duration = 0
    
    def _generate_id(self) -> str:
        return f"RTE{datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(100, 999)}"
    
    def add_point(self, point: TrackPoint):
        """Add a track point to the route"""
        self.points.append(point)
        self.updated_at = datetime.now()
        self._calculate_metrics()
    
    def _calculate_metrics(self):
        """Calculate route metrics"""
        if len(self.points) < 2:
            self.distance = 0
            self.duration = 0
            return
        
        # Calculate distance
        total_distance = 0
        for i in range(len(self.points) - 1):
            p1 = self.points[i]
            p2 = self.points[i + 1]
            total_distance += self._calculate_distance(p1.latitude, p1.longitude, 
                                                      p2.latitude, p2.longitude)
        
        self.distance = total_distance
        
        # Calculate duration
        if len(self.points) >= 2:
            self.duration = (self.points[-1].timestamp - self.points[0].timestamp).total_seconds()
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points"""
        R = 6371
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        return R * c
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'points': [p.to_dict() for p in self.points],
            'distance': self.distance,
            'duration': self.duration,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Route':
        route = cls(data['name'], data.get('description', ''))
        route.id = data['id']
        route.distance = data.get('distance', 0)
        route.duration = data.get('duration', 0)
        route.created_at = datetime.fromisoformat(data['created_at'])
        route.updated_at = datetime.fromisoformat(data['updated_at'])
        for point_data in data.get('points', []):
            route.points.append(TrackPoint.from_dict(point_data))
        return route

# ============================================================================
# STORAGE HANDLER
# ============================================================================

class StorageHandler:
    """Handles data persistence"""
    
    def __init__(self):
        self.data_dir = Path.home() / ".map_tracker"
        self.data_dir.mkdir(exist_ok=True)
        
        self.locations_file = self.data_dir / "locations.json"
        self.routes_file = self.data_dir / "routes.json"
        self.settings_file = self.data_dir / "settings.json"
    
    def save_locations(self, locations: List[dict]) -> bool:
        """Save locations to file"""
        try:
            with open(self.locations_file, 'w') as f:
                json.dump(locations, f, indent=2)
            return True
        except Exception:
            return False
    
    def load_locations(self) -> List[dict]:
        """Load locations from file"""
        if not self.locations_file.exists():
            return []
        try:
            with open(self.locations_file, 'r') as f:
                return json.load(f)
        except Exception:
            return []
    
    def save_routes(self, routes: List[dict]) -> bool:
        """Save routes to file"""
        try:
            with open(self.routes_file, 'w') as f:
                json.dump(routes, f, indent=2)
            return True
        except Exception:
            return False
    
    def load_routes(self) -> List[dict]:
        """Load routes from file"""
        if not self.routes_file.exists():
            return []
        try:
            with open(self.routes_file, 'r') as f:
                return json.load(f)
        except Exception:
            return []
    
    def save_settings(self, settings: dict) -> bool:
        """Save settings to file"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
            return True
        except Exception:
            return False
    
    def load_settings(self) -> dict:
        """Load settings from file"""
        if not self.settings_file.exists():
            return {'theme': 'light', 'units': 'metric', 'zoom': 10}
        try:
            with open(self.settings_file, 'r') as f:
                return json.load(f)
        except Exception:
            return {'theme': 'light', 'units': 'metric', 'zoom': 10}

# ============================================================================
# SERVICE LAYER
# ============================================================================

class MapTrackerService:
    """Service layer for map tracking operations"""
    
    def __init__(self):
        self.storage = StorageHandler()
        self.locations: Dict[str, Location] = {}
        self.routes: Dict[str, Route] = {}
        self.current_location = None
        self.is_tracking = False
        self.tracking_thread = None
        
        self._load_data()
    
    def _load_data(self):
        """Load all data from storage"""
        # Load locations
        loc_data = self.storage.load_locations()
        for data in loc_data:
            try:
                loc = Location.from_dict(data)
                self.locations[loc.id] = loc
            except Exception:
                continue
        
        # Load routes
        route_data = self.storage.load_routes()
        for data in route_data:
            try:
                route = Route.from_dict(data)
                self.routes[route.id] = route
            except Exception:
                continue
    
    def _save_all(self):
        """Save all data to storage"""
        loc_data = [loc.to_dict() for loc in self.locations.values()]
        self.storage.save_locations(loc_data)
        
        route_data = [route.to_dict() for route in self.routes.values()]
        self.storage.save_routes(route_data)
    
    # Location Operations
    def add_location(self, **kwargs) -> Location:
        """Add a new location"""
        loc = Location(**kwargs)
        self.locations[loc.id] = loc
        self._save_all()
        return loc
    
    def update_location(self, loc_id: str, **kwargs) -> Optional[Location]:
        """Update an existing location"""
        loc = self.locations.get(loc_id)
        if not loc:
            return None
        
        for key, value in kwargs.items():
            if hasattr(loc, key) and value is not None:
                setattr(loc, key, value)
        
        loc.updated_at = datetime.now()
        self._save_all()
        return loc
    
    def delete_location(self, loc_id: str) -> bool:
        """Delete a location"""
        if loc_id in self.locations:
            del self.locations[loc_id]
            self._save_all()
            return True
        return False
    
    def get_location(self, loc_id: str) -> Optional[Location]:
        """Get a location by ID"""
        return self.locations.get(loc_id)
    
    def get_all_locations(self, category: str = None) -> List[Location]:
        """Get all locations, optionally filtered by category"""
        locations = list(self.locations.values())
        if category:
            locations = [l for l in locations if l.category == category]
        return sorted(locations, key=lambda x: x.name)
    
    def get_categories(self) -> List[str]:
        """Get all unique categories"""
        categories = set()
        for loc in self.locations.values():
            categories.add(loc.category)
        return sorted(categories)
    
    def search_locations(self, query: str) -> List[Location]:
        """Search locations by name or address"""
        query = query.lower().strip()
        if not query:
            return []
        
        results = []
        for loc in self.locations.values():
            if query in loc.name.lower() or query in loc.address.lower():
                results.append(loc)
        return results
    
    def get_nearby_locations(self, lat: float, lon: float, radius_km: float = 10) -> List[Location]:
        """Find locations within a radius"""
        nearby = []
        for loc in self.locations.values():
            distance = loc.calculate_distance(lat, lon)
            if distance <= radius_km:
                nearby.append((loc, distance))
        nearby.sort(key=lambda x: x[1])
        return [loc for loc, dist in nearby]
    
    def record_visit(self, loc_id: str) -> bool:
        """Record a visit to a location"""
        loc = self.locations.get(loc_id)
        if not loc:
            return False
        
        loc.visit_count += 1
        loc.last_visited = datetime.now()
        self._save_all()
        return True
    
    # Route Operations
    def create_route(self, name: str, description: str = "") -> Route:
        """Create a new route"""
        route = Route(name, description)
        self.routes[route.id] = route
        self._save_all()
        return route
    
    def add_point_to_route(self, route_id: str, lat: float, lon: float, speed: float = 0, altitude: float = 0) -> bool:
        """Add a point to a route"""
        route = self.routes.get(route_id)
        if not route:
            return False
        
        point = TrackPoint(lat, lon, speed, altitude)
        route.add_point(point)
        self._save_all()
        return True
    
    def get_route(self, route_id: str) -> Optional[Route]:
        """Get a route by ID"""
        return self.routes.get(route_id)
    
    def get_all_routes(self) -> List[Route]:
        """Get all routes"""
        return list(self.routes.values())
    
    def delete_route(self, route_id: str) -> bool:
        """Delete a route"""
        if route_id in self.routes:
            del self.routes[route_id]
            self._save_all()
            return True
        return False
    
    def get_route_statistics(self, route_id: str) -> dict:
        """Get statistics for a route"""
        route = self.routes.get(route_id)
        if not route:
            return {}
        
        if not route.points:
            return {'points': 0, 'distance': 0, 'duration': 0, 'speed': 0}
        
        duration_hours = route.duration / 3600
        avg_speed = route.distance / duration_hours if duration_hours > 0 else 0
        
        return {
            'points': len(route.points),
            'distance_km': route.distance,
            'duration_seconds': route.duration,
            'duration_formatted': self._format_duration(route.duration),
            'avg_speed_kmh': avg_speed,
            'start_time': route.points[0].timestamp,
            'end_time': route.points[-1].timestamp
        }
    
    def _format_duration(self, seconds: float) -> str:
        """Format duration in seconds to readable string"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        
        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"
    
    # Tracking Simulation
    def start_tracking(self, callback):
        """Start simulated tracking"""
        if self.is_tracking:
            return
        
        self.is_tracking = True
        self.tracking_thread = threading.Thread(
            target=self._tracking_simulation,
            args=(callback,),
            daemon=True
        )
        self.tracking_thread.start()
    
    def stop_tracking(self):
        """Stop tracking"""
        self.is_tracking = False
        if self.tracking_thread:
            self.tracking_thread.join(timeout=1)
    
    def _tracking_simulation(self, callback):
        """Simulate GPS tracking"""
        # Start from a random location
        lat = random.uniform(37.0, 38.0)
        lon = random.uniform(-122.5, -121.5)
        
        # Generate a route with random movement
        steps = random.randint(20, 50)
        
        for i in range(steps):
            if not self.is_tracking:
                break
            
            # Random walk
            lat += random.uniform(-0.01, 0.01)
            lon += random.uniform(-0.01, 0.01)
            
            # Simulate speed
            speed = random.uniform(0, 50)  # km/h
            
            # Simulate altitude
            altitude = random.uniform(0, 1000)  # meters
            
            # Update current location
            self.current_location = (lat, lon, speed, altitude)
            
            # Call callback with new data
            callback(lat, lon, speed, altitude)
            
            # Wait between points
            time.sleep(1)
        
        self.is_tracking = False

# ============================================================================
# UI LAYER - MAIN APPLICATION
# ============================================================================

class MapTrackerApp:
    """Main application with beautiful UI"""
    
    COLORS = {
        'primary': '#2196F3',
        'primary_dark': '#1976D2',
        'primary_light': '#BBDEFB',
        'secondary': '#FF9800',
        'success': '#4CAF50',
        'danger': '#F44336',
        'warning': '#FFC107',
        'info': '#00BCD4',
        'dark': '#263238',
        'light': '#ECEFF1',
        'white': '#FFFFFF',
        'gray': '#78909C',
        'background': '#F5F5F5',
        'card': '#FFFFFF',
        'border': '#DEE2E6',  # Added missing color
        'shadow': '#0000001A',
        'light_gray': '#E0E0E0'  # Added for canvas grid
    }
    
    FONTS = {
        'title': ('Segoe UI', 24, 'bold'),
        'heading': ('Segoe UI', 16, 'bold'),
        'subheading': ('Segoe UI', 14, 'bold'),
        'body': ('Segoe UI', 11),
        'body_bold': ('Segoe UI', 11, 'bold'),
        'small': ('Segoe UI', 9),
        'small_bold': ('Segoe UI', 9, 'bold'),
        'mono': ('Consolas', 10)
    }
    
    def __init__(self, root):
        self.root = root
        self.root.title("🗺️ Map Tracker")
        self.root.geometry("1400x800")
        self.root.minsize(1200, 700)
        self.root.configure(bg=self.COLORS['background'])
        
        # Initialize service
        self.service = MapTrackerService()
        
        # Tracking state
        self.is_tracking = False
        self.track_points = []
        self.settings = self.service.storage.load_settings()
        
        # Setup UI
        self._setup_styles()
        self._create_widgets()
        self._load_data()
        
        # Center window
        self._center_window()
        
        # Start with demo locations
        self._create_demo_locations()
    
    def _center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def _setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure Treeview
        style.configure('Treeview',
                       background=self.COLORS['white'],
                       foreground=self.COLORS['dark'],
                       rowheight=35,
                       font=self.FONTS['body'])
        style.configure('Treeview.Heading',
                       background=self.COLORS['primary'],
                       foreground=self.COLORS['white'],
                       font=self.FONTS['body_bold'])
    
    def _create_widgets(self):
        """Create all UI widgets"""
        # Main container
        self.main_container = tk.Frame(self.root, bg=self.COLORS['background'])
        self.main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        self._create_header()
        
        # Content (split into 3 sections)
        self.content_frame = tk.Frame(self.main_container, bg=self.COLORS['background'])
        self.content_frame.pack(fill='both', expand=True, pady=10)
        
        # Left: Locations list
        self._create_location_list()
        
        # Center: Map display
        self._create_map_display()
        
        # Right: Details panel
        self._create_details_panel()
        
        # Status bar
        self._create_status_bar()
    
    def _create_header(self):
        """Create the header with controls"""
        header = tk.Frame(self.main_container, bg=self.COLORS['primary'], height=70)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Title
        title = tk.Label(header,
                        text="🗺️ Map Tracker",
                        font=self.FONTS['title'],
                        bg=self.COLORS['primary'],
                        fg=self.COLORS['white'])
        title.pack(side='left', padx=20, pady=15)
        
        # Controls
        controls = tk.Frame(header, bg=self.COLORS['primary'])
        controls.pack(side='right', padx=20)
        
        # Start/Stop tracking button
        self.track_btn = tk.Button(controls,
                                   text="▶ Start Tracking",
                                   font=self.FONTS['body_bold'],
                                   bg=self.COLORS['secondary'],
                                   fg=self.COLORS['white'],
                                   relief='flat',
                                   padx=20,
                                   pady=8,
                                   cursor='hand2',
                                   command=self._toggle_tracking)
        self.track_btn.pack(side='left', padx=5)
        self._add_hover_effect(self.track_btn, self.COLORS['secondary'], '#F57C00')
        
        # Add location button
        add_btn = tk.Button(controls,
                           text="➕ Add Location",
                           font=self.FONTS['body_bold'],
                           bg=self.COLORS['success'],
                           fg=self.COLORS['white'],
                           relief='flat',
                           padx=20,
                           pady=8,
                           cursor='hand2',
                           command=self._add_location)
        add_btn.pack(side='left', padx=5)
        self._add_hover_effect(add_btn, self.COLORS['success'], '#388E3C')
        
        # Refresh button
        refresh_btn = tk.Button(controls,
                               text="🔄 Refresh",
                               font=self.FONTS['body'],
                               bg=self.COLORS['info'],
                               fg=self.COLORS['white'],
                               relief='flat',
                               padx=15,
                               pady=8,
                               cursor='hand2',
                               command=self._refresh_data)
        refresh_btn.pack(side='left', padx=5)
        self._add_hover_effect(refresh_btn, self.COLORS['info'], '#00838F')
    
    def _create_location_list(self):
        """Create the location list panel"""
        left_panel = tk.Frame(self.content_frame, bg=self.COLORS['white'], relief='flat', bd=1)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 5))
        left_panel.configure(highlightbackground=self.COLORS['border'], highlightthickness=1)
        
        # Header
        tk.Label(left_panel,
                text="📍 Locations",
                font=self.FONTS['heading'],
                bg=self.COLORS['white'],
                fg=self.COLORS['dark']).pack(anchor='w', padx=15, pady=10)
        
        # Search bar
        search_frame = tk.Frame(left_panel, bg=self.COLORS['white'])
        search_frame.pack(fill='x', padx=15, pady=(0, 10))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self._search_locations())
        
        search_entry = tk.Entry(search_frame,
                               textvariable=self.search_var,
                               font=self.FONTS['body'],
                               bg=self.COLORS['light'],
                               relief='flat',
                               bd=0,
                               highlightthickness=1,
                               highlightcolor=self.COLORS['primary'])
        search_entry.pack(fill='x', ipady=5)
        search_entry.insert(0, "🔍 Search locations...")
        search_entry.bind('<FocusIn>', lambda e: search_entry.delete(0, tk.END) if search_entry.get() == "🔍 Search locations..." else None)
        
        # Category filter
        filter_frame = tk.Frame(left_panel, bg=self.COLORS['white'])
        filter_frame.pack(fill='x', padx=15, pady=(0, 10))
        
        tk.Label(filter_frame,
                text="Filter:",
                font=self.FONTS['body'],
                bg=self.COLORS['white']).pack(side='left', padx=(0, 5))
        
        self.category_var = tk.StringVar(value="All")
        self.category_menu = ttk.Combobox(filter_frame,
                                         textvariable=self.category_var,
                                         font=self.FONTS['body'],
                                         state='readonly',
                                         width=15)
        self.category_menu.pack(side='left', padx=5)
        self.category_menu.bind('<<ComboboxSelected>>', lambda e: self._filter_locations())
        
        # Location tree
        tree_frame = tk.Frame(left_panel, bg=self.COLORS['white'])
        tree_frame.pack(fill='both', expand=True, padx=15, pady=(0, 10))
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.loc_tree = ttk.Treeview(tree_frame,
                                     columns=('name', 'category', 'distance'),
                                     show='headings',
                                     yscrollcommand=scrollbar.set,
                                     selectmode='browse')
        
        self.loc_tree.heading('name', text='Name', anchor='w')
        self.loc_tree.heading('category', text='Category', anchor='w')
        self.loc_tree.heading('distance', text='Distance', anchor='w')
        
        self.loc_tree.column('name', width=150)
        self.loc_tree.column('category', width=80)
        self.loc_tree.column('distance', width=80)
        
        self.loc_tree.pack(fill='both', expand=True)
        scrollbar.config(command=self.loc_tree.yview)
        
        # Bind selection
        self.loc_tree.bind('<<TreeviewSelect>>', self._on_location_select)
    
    def _create_map_display(self):
        """Create the map display panel"""
        center_panel = tk.Frame(self.content_frame, bg=self.COLORS['white'], relief='flat', bd=1)
        center_panel.pack(side='left', fill='both', expand=True, padx=5)
        center_panel.configure(highlightbackground=self.COLORS['border'], highlightthickness=1)
        
        # Header
        map_header = tk.Frame(center_panel, bg=self.COLORS['white'])
        map_header.pack(fill='x', padx=15, pady=10)
        
        tk.Label(map_header,
                text="🗺️ Map View",
                font=self.FONTS['heading'],
                bg=self.COLORS['white'],
                fg=self.COLORS['dark']).pack(side='left')
        
        # Map controls
        map_controls = tk.Frame(map_header, bg=self.COLORS['white'])
        map_controls.pack(side='right')
        
        tk.Button(map_controls,
                 text="🌐 Open in Browser",
                 font=self.FONTS['small'],
                 bg=self.COLORS['info'],
                 fg=self.COLORS['white'],
                 relief='flat',
                 padx=10,
                 pady=5,
                 cursor='hand2',
                 command=self._open_in_browser).pack(side='left', padx=5)
        
        # Canvas for map simulation
        self.map_canvas = tk.Canvas(center_panel,
                                   bg=self.COLORS['light'],
                                   highlightthickness=0,
                                   relief='flat')
        self.map_canvas.pack(fill='both', expand=True, padx=15, pady=(0, 10))
        
        # Draw initial map
        self._draw_map()
        
        # Bind resize
        self.map_canvas.bind('<Configure>', lambda e: self._draw_map())
        
        # Click handler for adding locations
        self.map_canvas.bind('<Double-Button-1>', self._on_map_double_click)
    
    def _create_details_panel(self):
        """Create the details panel"""
        right_panel = tk.Frame(self.content_frame, bg=self.COLORS['white'], relief='flat', bd=1)
        right_panel.pack(side='right', fill='both', expand=True, padx=(5, 0))
        right_panel.configure(highlightbackground=self.COLORS['border'], highlightthickness=1)
        
        # Header
        header_frame = tk.Frame(right_panel, bg=self.COLORS['white'])
        header_frame.pack(fill='x', padx=15, pady=10)
        
        tk.Label(header_frame,
                text="📋 Details",
                font=self.FONTS['heading'],
                bg=self.COLORS['white'],
                fg=self.COLORS['dark']).pack(side='left')
        
        # Content with scrollbar
        details_container = tk.Frame(right_panel, bg=self.COLORS['white'])
        details_container.pack(fill='both', expand=True, padx=15, pady=(0, 10))
        
        canvas = tk.Canvas(details_container, bg=self.COLORS['white'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(details_container, orient='vertical', command=canvas.yview)
        
        self.details_frame = tk.Frame(canvas, bg=self.COLORS['white'])
        self.details_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        
        canvas.create_window((0, 0), window=self.details_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Initial details
        self._show_empty_details()
    
    def _create_status_bar(self):
        """Create the status bar"""
        status = tk.Frame(self.main_container, bg=self.COLORS['dark'], height=30)
        status.pack(side='bottom', fill='x')
        status.pack_propagate(False)
        
        # Status label
        self.status_label = tk.Label(status,
                                     text="✅ Ready",
                                     font=self.FONTS['small'],
                                     bg=self.COLORS['dark'],
                                     fg=self.COLORS['white'],
                                     anchor='w')
        self.status_label.pack(side='left', padx=10)
        
        # Location info
        self.location_status = tk.Label(status,
                                        text="📍 No location selected",
                                        font=self.FONTS['small'],
                                        bg=self.COLORS['dark'],
                                        fg=self.COLORS['white'],
                                        anchor='e')
        self.location_status.pack(side='right', padx=10)
        
        # Tracking status
        self.tracking_status = tk.Label(status,
                                        text="⏹️ Stopped",
                                        font=self.FONTS['small'],
                                        bg=self.COLORS['dark'],
                                        fg=self.COLORS['white'],
                                        anchor='e')
        self.tracking_status.pack(side='right', padx=10)
    
    # ========================================================================
    # UI Helper Methods
    # ========================================================================
    
    def _add_hover_effect(self, button, normal_color, hover_color):
        """Add hover effect to a button"""
        def on_enter(e):
            if button['state'] != 'disabled':
                button['background'] = hover_color
        
        def on_leave(e):
            if button['state'] != 'disabled':
                button['background'] = normal_color
        
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)
    
    def _set_status(self, message, is_error=False):
        """Set status bar message"""
        color = self.COLORS['danger'] if is_error else self.COLORS['white']
        self.status_label.config(text=f"{'❌' if is_error else '✅'} {message}", fg=color)
    
    # ========================================================================
    # Map Drawing Methods
    # ========================================================================
    
    def _draw_map(self, locations=None):
        """Draw the map with locations"""
        canvas = self.map_canvas
        canvas.delete('all')
        
        # Get canvas dimensions
        width = canvas.winfo_width() if canvas.winfo_width() > 1 else 800
        height = canvas.winfo_height() if canvas.winfo_height() > 1 else 500
        
        # Draw grid (simulated map background)
        for x in range(0, width, 50):
            canvas.create_line(x, 0, x, height, fill=self.COLORS['light_gray'], width=1)
        for y in range(0, height, 50):
            canvas.create_line(0, y, width, y, fill=self.COLORS['light_gray'], width=1)
        
        # Draw a subtle gradient
        for i in range(10):
            alpha = 1.0 - (i / 10)
            color = f'#{int(200 - i*20):02x}{int(200 - i*20):02x}{int(230 - i*20):02x}'
            canvas.create_rectangle(0, i*height//10, width, (i+1)*height//10,
                                   fill=color, outline='')
        
        # Get locations to display
        if locations is None:
            locations = self.service.get_all_locations()
        
        # Draw locations
        if locations:
            # Calculate bounds
            min_lat = min(l.latitude for l in locations)
            max_lat = max(l.latitude for l in locations)
            min_lon = min(l.longitude for l in locations)
            max_lon = max(l.longitude for l in locations)
            
            # Add padding
            lat_range = max_lat - min_lat or 1
            lon_range = max_lon - min_lon or 1
            padding = 0.1
            
            min_lat -= lat_range * padding
            max_lat += lat_range * padding
            min_lon -= lon_range * padding
            max_lon += lon_range * padding
            
            for loc in locations:
                # Convert lat/lon to canvas coordinates
                x = ((loc.longitude - min_lon) / (max_lon - min_lon)) * width
                y = ((loc.latitude - min_lat) / (max_lat - min_lat)) * height
                y = height - y  # Flip y-axis
                
                # Draw location marker
                radius = 12 if loc.is_favorite else 8
                color = self.COLORS['primary'] if not loc.is_favorite else self.COLORS['warning']
                
                # Glow effect
                canvas.create_oval(x - radius*2, y - radius*2,
                                  x + radius*2, y + radius*2,
                                  fill=self.COLORS['primary_light'],
                                  outline='',
                                  stipple='gray50')
                
                # Main circle
                canvas.create_oval(x - radius, y - radius,
                                  x + radius, y + radius,
                                  fill=color, outline=self.COLORS['white'],
                                  width=2)
                
                # Inner dot
                canvas.create_oval(x - 3, y - 3,
                                  x + 3, y + 3,
                                  fill=self.COLORS['white'])
                
                # Label
                canvas.create_text(x + radius + 8, y,
                                  text=loc.name[:15],
                                  font=self.FONTS['small'],
                                  fill=self.COLORS['dark'],
                                  anchor='w')
        
        # Draw current location if tracking
        if self.is_tracking and self.service.current_location:
            lat, lon, speed, altitude = self.service.current_location
            x = ((lon - min_lon) / (max_lon - min_lon)) * width
            y = ((lat - min_lat) / (max_lat - min_lat)) * height
            y = height - y
            
            # Pulsing circle animation
            pulse_size = 15 + (datetime.now().second % 5) * 3
            canvas.create_oval(x - pulse_size, y - pulse_size,
                              x + pulse_size, y + pulse_size,
                              fill='', outline=self.COLORS['danger'],
                              width=3, tags=('pulse',))
            
            # Current position marker
            canvas.create_oval(x - 8, y - 8, x + 8, y + 8,
                              fill=self.COLORS['danger'],
                              outline=self.COLORS['white'],
                              width=2)
            
            canvas.create_text(x, y - 20,
                              text="📍 You are here",
                              font=self.FONTS['small_bold'],
                              fill=self.COLORS['danger'])
        
        # Draw tracking path
        if self.track_points:
            min_lat = min(p[0] for p in self.track_points)
            max_lat = max(p[0] for p in self.track_points)
            min_lon = min(p[1] for p in self.track_points)
            max_lon = max(p[1] for p in self.track_points)
            
            lat_range = max_lat - min_lat or 1
            lon_range = max_lon - min_lon or 1
            
            for i in range(len(self.track_points) - 1):
                x1 = ((self.track_points[i][1] - min_lon) / lon_range) * width
                y1 = height - ((self.track_points[i][0] - min_lat) / lat_range) * height
                x2 = ((self.track_points[i+1][1] - min_lon) / lon_range) * width
                y2 = height - ((self.track_points[i+1][0] - min_lat) / lat_range) * height
                
                canvas.create_line(x1, y1, x2, y2,
                                  fill=self.COLORS['danger'],
                                  width=3,
                                  dash=(5, 5))
    
    def _open_in_browser(self):
        """Open current location in web browser"""
        if self.loc_tree.selection():
            item = self.loc_tree.selection()[0]
            loc_id = self.loc_tree.item(item, 'tags')[0]
            loc = self.service.get_location(loc_id)
            if loc:
                url = f"https://www.openstreetmap.org/?mlat={loc.latitude}&mlon={loc.longitude}&zoom=15"
                webbrowser.open(url)
                self._set_status(f"Opened {loc.name} in browser")
        else:
            messagebox.showinfo("Info", "Please select a location first")
    
    # ========================================================================
    # Location Management Methods
    # ========================================================================
    
    def _load_data(self):
        """Load and display all data"""
        self._load_categories()
        self._load_locations()
    
    def _load_categories(self):
        """Load categories into filter dropdown"""
        categories = self.service.get_categories()
        categories.insert(0, "All")
        self.category_menu['values'] = categories
    
    def _load_locations(self):
        """Load locations into treeview"""
        # Clear tree
        for item in self.loc_tree.get_children():
            self.loc_tree.delete(item)
        
        # Get locations
        category = self.category_var.get()
        if category == "All":
            locations = self.service.get_all_locations()
        else:
            locations = [l for l in self.service.get_all_locations() if l.category == category]
        
        # Add to tree
        for loc in locations:
            self.loc_tree.insert('', 'end',
                               values=(loc.name, loc.category, ''),
                               tags=(loc.id,))
        
        self._set_status(f"Loaded {len(locations)} locations")
    
    def _search_locations(self):
        """Search locations"""
        query = self.search_var.get()
        if query == "🔍 Search locations...":
            query = ""
        
        # Clear tree
        for item in self.loc_tree.get_children():
            self.loc_tree.delete(item)
        
        # Search
        results = self.service.search_locations(query) if query else self.service.get_all_locations()
        
        # Filter by category
        category = self.category_var.get()
        if category != "All":
            results = [l for l in results if l.category == category]
        
        # Add to tree
        for loc in results:
            self.loc_tree.insert('', 'end',
                               values=(loc.name, loc.category, ''),
                               tags=(loc.id,))
    
    def _filter_locations(self):
        """Filter locations by category"""
        self._load_locations()
    
    def _on_location_select(self, event):
        """Handle location selection"""
        if not self.loc_tree.selection():
            return
        
        item = self.loc_tree.selection()[0]
        loc_id = self.loc_tree.item(item, 'tags')[0]
        loc = self.service.get_location(loc_id)
        
        if loc:
            self._show_location_details(loc)
            self._set_status(f"Selected: {loc.name}")
            self.location_status.config(text=f"📍 {loc.name}")
    
    def _show_location_details(self, loc: Location):
        """Show location details in the details panel"""
        # Clear existing details
        for widget in self.details_frame.winfo_children():
            widget.destroy()
        
        # Name
        name_frame = tk.Frame(self.details_frame, bg=self.COLORS['white'])
        name_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(name_frame,
                text=loc.name,
                font=self.FONTS['heading'],
                bg=self.COLORS['white'],
                fg=self.COLORS['dark']).pack(side='left')
        
        # Favorite star
        star = "⭐" if loc.is_favorite else "☆"
        fav_btn = tk.Button(name_frame,
                           text=star,
                           font=('Segoe UI', 16),
                           bg=self.COLORS['white'],
                           fg=self.COLORS['warning'] if loc.is_favorite else self.COLORS['gray'],
                           relief='flat',
                           cursor='hand2',
                           command=lambda: self._toggle_favorite(loc.id))
        fav_btn.pack(side='right')
        
        # Details in a grid
        details = [
            ("📍 Category", loc.category),
            ("📌 Address", loc.address or "Not specified"),
            ("🌐 Latitude", f"{loc.latitude:.6f}"),
            ("🌐 Longitude", f"{loc.longitude:.6f}"),
            ("📝 Description", loc.description or "No description"),
            ("📊 Visit Count", str(loc.visit_count)),
            ("🕐 Last Visit", loc.last_visited.strftime('%Y-%m-%d %H:%M') if loc.last_visited else "Never"),
            ("📅 Created", loc.created_at.strftime('%Y-%m-%d %H:%M')),
            ("🔄 Updated", loc.updated_at.strftime('%Y-%m-%d %H:%M'))
        ]
        
        for i, (label, value) in enumerate(details):
            frame = tk.Frame(self.details_frame, bg=self.COLORS['white'])
            frame.pack(fill='x', pady=3)
            
            tk.Label(frame,
                    text=label,
                    font=self.FONTS['body_bold'],
                    bg=self.COLORS['white'],
                    fg=self.COLORS['gray'],
                    width=15,
                    anchor='w').pack(side='left')
            
            tk.Label(frame,
                    text=value,
                    font=self.FONTS['body'],
                    bg=self.COLORS['white'],
                    fg=self.COLORS['dark'],
                    anchor='w').pack(side='left', fill='x', expand=True)
        
        # Tags
        if loc.tags:
            tag_frame = tk.Frame(self.details_frame, bg=self.COLORS['white'])
            tag_frame.pack(fill='x', pady=10)
            
            tk.Label(tag_frame,
                    text="🏷️ Tags:",
                    font=self.FONTS['body_bold'],
                    bg=self.COLORS['white'],
                    fg=self.COLORS['gray'],
                    width=15,
                    anchor='w').pack(side='left')
            
            for tag in loc.tags:
                tk.Label(tag_frame,
                        text=f"#{tag}",
                        font=self.FONTS['small'],
                        bg=self.COLORS['primary_light'],
                        fg=self.COLORS['white'],
                        padx=8,
                        pady=2,
                        relief='flat').pack(side='left', padx=2)
        
        # Buttons
        btn_frame = tk.Frame(self.details_frame, bg=self.COLORS['white'])
        btn_frame.pack(fill='x', pady=(10, 0))
        
        tk.Button(btn_frame,
                 text="✏️ Edit",
                 font=self.FONTS['body'],
                 bg=self.COLORS['primary'],
                 fg=self.COLORS['white'],
                 relief='flat',
                 padx=15,
                 pady=5,
                 cursor='hand2',
                 command=lambda: self._edit_location(loc.id)).pack(side='left', padx=2)
        
        tk.Button(btn_frame,
                 text="🗑️ Delete",
                 font=self.FONTS['body'],
                 bg=self.COLORS['danger'],
                 fg=self.COLORS['white'],
                 relief='flat',
                 padx=15,
                 pady=5,
                 cursor='hand2',
                 command=lambda: self._delete_location(loc.id)).pack(side='left', padx=2)
        
        tk.Button(btn_frame,
                 text="📍 Visit",
                 font=self.FONTS['body'],
                 bg=self.COLORS['success'],
                 fg=self.COLORS['white'],
                 relief='flat',
                 padx=15,
                 pady=5,
                 cursor='hand2',
                 command=lambda: self._record_visit(loc.id)).pack(side='left', padx=2)
        
        tk.Button(btn_frame,
                 text="🌐 Map",
                 font=self.FONTS['body'],
                 bg=self.COLORS['info'],
                 fg=self.COLORS['white'],
                 relief='flat',
                 padx=15,
                 pady=5,
                 cursor='hand2',
                 command=self._open_in_browser).pack(side='left', padx=2)
        
        # Nearby locations
        if loc:
            nearby = self.service.get_nearby_locations(loc.latitude, loc.longitude, 20)
            nearby = [l for l in nearby if l.id != loc.id]
            if nearby:
                tk.Label(self.details_frame,
                        text=f"\n📍 Nearby Locations ({len(nearby)})",
                        font=self.FONTS['subheading'],
                        bg=self.COLORS['white'],
                        fg=self.COLORS['dark']).pack(anchor='w', pady=(15, 5))
                
                for nloc in nearby[:5]:
                    distance = nloc.calculate_distance(loc.latitude, loc.longitude)
                    tk.Label(self.details_frame,
                            text=f"  • {nloc.name} ({distance:.1f} km)",
                            font=self.FONTS['body'],
                            bg=self.COLORS['white'],
                            fg=self.COLORS['dark']).pack(anchor='w')
    
    def _show_empty_details(self):
        """Show empty details message"""
        for widget in self.details_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.details_frame,
                text="No Location Selected",
                font=self.FONTS['heading'],
                bg=self.COLORS['white'],
                fg=self.COLORS['gray']).pack(pady=50)
        
        tk.Label(self.details_frame,
                text="Select a location from the list\nor double-click on the map to add one",
                font=self.FONTS['body'],
                bg=self.COLORS['white'],
                fg=self.COLORS['gray'],
                justify='center').pack()
    
    # ========================================================================
    # Location Operations
    # ========================================================================
    
    def _add_location(self):
        """Add a new location"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Location")
        dialog.geometry("500x600")
        dialog.configure(bg=self.COLORS['white'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (600 // 2)
        dialog.geometry(f"500x600+{x}+{y}")
        
        # Title
        tk.Label(dialog,
                text="➕ Add New Location",
                font=self.FONTS['title'],
                bg=self.COLORS['white'],
                fg=self.COLORS['primary']).pack(pady=20)
        
        # Form
        form = tk.Frame(dialog, bg=self.COLORS['white'])
        form.pack(fill='both', expand=True, padx=30)
        
        # Fields
        fields = [
            ('name', "Location Name *"),
            ('latitude', "Latitude *"),
            ('longitude', "Longitude *"),
            ('address', "Address"),
            ('category', "Category"),
            ('description', "Description"),
            ('tags', "Tags (comma-separated)")
        ]
        
        entries = {}
        
        for i, (field, label) in enumerate(fields):
            tk.Label(form,
                    text=label,
                    font=self.FONTS['body_bold'],
                    bg=self.COLORS['white'],
                    fg=self.COLORS['dark']).grid(row=i, column=0, sticky='w', pady=(5, 2))
            
            if field == 'description':
                entry = scrolledtext.ScrolledText(form,
                                                 height=3,
                                                 font=self.FONTS['body'],
                                                 bg=self.COLORS['light'],
                                                 relief='flat',
                                                 bd=0,
                                                 highlightthickness=1,
                                                 highlightcolor=self.COLORS['primary'])
                entry.grid(row=i, column=1, sticky='ew', pady=(5, 2), padx=(10, 0))
                entries[field] = entry
            else:
                var = tk.StringVar()
                entry = tk.Entry(form,
                                textvariable=var,
                                font=self.FONTS['body'],
                                bg=self.COLORS['light'],
                                relief='flat',
                                bd=0,
                                highlightthickness=1,
                                highlightcolor=self.COLORS['primary'])
                entry.grid(row=i, column=1, sticky='ew', pady=(5, 2), padx=(10, 0))
                entries[field] = var
        
        # Set default category
        categories = self.service.get_categories()
        if categories:
            entries['category'].set(categories[0])
        
        # Buttons
        btn_frame = tk.Frame(dialog, bg=self.COLORS['white'])
        btn_frame.pack(fill='x', padx=30, pady=20)
        
        def save_location():
            try:
                name = entries['name'].get().strip()
                lat = float(entries['latitude'].get())
                lon = float(entries['longitude'].get())
                address = entries['address'].get().strip()
                category = entries['category'].get().strip()
                description = entries['description'].get('1.0', tk.END).strip()
                tags = [t.strip() for t in entries['tags'].get().split(',') if t.strip()]
                
                if not name:
                    messagebox.showerror("Error", "Location name is required")
                    return
                
                loc = self.service.add_location(
                    name=name,
                    latitude=lat,
                    longitude=lon,
                    address=address,
                    category=category or "General",
                    description=description,
                    tags=tags
                )
                
                self._load_data()
                self._draw_map()
                dialog.destroy()
                messagebox.showinfo("Success", f"Added location: {loc.name}")
                
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid number format: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add location: {e}")
        
        tk.Button(btn_frame,
                 text="💾 Save Location",
                 font=self.FONTS['body_bold'],
                 bg=self.COLORS['primary'],
                 fg=self.COLORS['white'],
                 relief='flat',
                 padx=30,
                 pady=10,
                 cursor='hand2',
                 command=save_location).pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        tk.Button(btn_frame,
                 text="Cancel",
                 font=self.FONTS['body'],
                 bg=self.COLORS['light'],
                 fg=self.COLORS['dark'],
                 relief='flat',
                 padx=30,
                 pady=10,
                 cursor='hand2',
                 command=dialog.destroy).pack(side='left', fill='x', expand=True, padx=(5, 0))
        
        # Configure grid
        form.grid_columnconfigure(1, weight=1)
    
    def _edit_location(self, loc_id: str):
        """Edit an existing location"""
        loc = self.service.get_location(loc_id)
        if not loc:
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Location")
        dialog.geometry("500x600")
        dialog.configure(bg=self.COLORS['white'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (600 // 2)
        dialog.geometry(f"500x600+{x}+{y}")
        
        # Title
        tk.Label(dialog,
                text=f"✏️ Edit Location: {loc.name}",
                font=self.FONTS['title'],
                bg=self.COLORS['white'],
                fg=self.COLORS['primary']).pack(pady=20)
        
        # Form
        form = tk.Frame(dialog, bg=self.COLORS['white'])
        form.pack(fill='both', expand=True, padx=30)
        
        # Fields
        fields = [
            ('name', "Location Name *"),
            ('latitude', "Latitude *"),
            ('longitude', "Longitude *"),
            ('address', "Address"),
            ('category', "Category"),
            ('description', "Description"),
            ('tags', "Tags (comma-separated)")
        ]
        
        entries = {}
        
        for i, (field, label) in enumerate(fields):
            tk.Label(form,
                    text=label,
                    font=self.FONTS['body_bold'],
                    bg=self.COLORS['white'],
                    fg=self.COLORS['dark']).grid(row=i, column=0, sticky='w', pady=(5, 2))
            
            if field == 'description':
                entry = scrolledtext.ScrolledText(form,
                                                 height=3,
                                                 font=self.FONTS['body'],
                                                 bg=self.COLORS['light'],
                                                 relief='flat',
                                                 bd=0,
                                                 highlightthickness=1,
                                                 highlightcolor=self.COLORS['primary'])
                entry.grid(row=i, column=1, sticky='ew', pady=(5, 2), padx=(10, 0))
                entry.insert('1.0', getattr(loc, field))
                entries[field] = entry
            else:
                var = tk.StringVar(value=getattr(loc, field))
                entry = tk.Entry(form,
                                textvariable=var,
                                font=self.FONTS['body'],
                                bg=self.COLORS['light'],
                                relief='flat',
                                bd=0,
                                highlightthickness=1,
                                highlightcolor=self.COLORS['primary'])
                entry.grid(row=i, column=1, sticky='ew', pady=(5, 2), padx=(10, 0))
                entries[field] = var
        
        # Buttons
        btn_frame = tk.Frame(dialog, bg=self.COLORS['white'])
        btn_frame.pack(fill='x', padx=30, pady=20)
        
        def save_changes():
            try:
                name = entries['name'].get().strip()
                lat = float(entries['latitude'].get())
                lon = float(entries['longitude'].get())
                address = entries['address'].get().strip()
                category = entries['category'].get().strip()
                description = entries['description'].get('1.0', tk.END).strip()
                tags = [t.strip() for t in entries['tags'].get().split(',') if t.strip()]
                
                if not name:
                    messagebox.showerror("Error", "Location name is required")
                    return
                
                self.service.update_location(
                    loc_id,
                    name=name,
                    latitude=lat,
                    longitude=lon,
                    address=address,
                    category=category or "General",
                    description=description,
                    tags=tags
                )
                
                self._load_data()
                self._draw_map()
                dialog.destroy()
                messagebox.showinfo("Success", f"Updated location: {name}")
                
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid number format: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update location: {e}")
        
        tk.Button(btn_frame,
                 text="💾 Save Changes",
                 font=self.FONTS['body_bold'],
                 bg=self.COLORS['primary'],
                 fg=self.COLORS['white'],
                 relief='flat',
                 padx=30,
                 pady=10,
                 cursor='hand2',
                 command=save_changes).pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        tk.Button(btn_frame,
                 text="Cancel",
                 font=self.FONTS['body'],
                 bg=self.COLORS['light'],
                 fg=self.COLORS['dark'],
                 relief='flat',
                 padx=30,
                 pady=10,
                 cursor='hand2',
                 command=dialog.destroy).pack(side='left', fill='x', expand=True, padx=(5, 0))
        
        form.grid_columnconfigure(1, weight=1)
    
    def _delete_location(self, loc_id: str):
        """Delete a location"""
        loc = self.service.get_location(loc_id)
        if not loc:
            return
        
        if messagebox.askyesno("Delete Location", f"Are you sure you want to delete '{loc.name}'?"):
            self.service.delete_location(loc_id)
            self._load_data()
            self._draw_map()
            self._show_empty_details()
            messagebox.showinfo("Success", "Location deleted")
    
    def _toggle_favorite(self, loc_id: str):
        """Toggle favorite status"""
        loc = self.service.get_location(loc_id)
        if not loc:
            return
        
        loc.is_favorite = not loc.is_favorite
        self.service.update_location(loc_id, is_favorite=loc.is_favorite)
        self._show_location_details(loc)
        self._load_data()
        self._draw_map()
    
    def _record_visit(self, loc_id: str):
        """Record a visit to a location"""
        self.service.record_visit(loc_id)
        loc = self.service.get_location(loc_id)
        if loc:
            self._show_location_details(loc)
            messagebox.showinfo("Visit Recorded", f"Visited {loc.name}!")
    
    def _on_map_double_click(self, event):
        """Handle double-click on map to add location"""
        # Get approximate coordinates from canvas position
        # This is a simplified version - in a real app, you'd use reverse geocoding
        lat = 37.0 + (event.y / 1000)  # Simulated latitude
        lon = -122.0 + (event.x / 1000)  # Simulated longitude
        
        # Open add dialog with coordinates pre-filled
        self._add_location_with_coords(lat, lon)
    
    def _add_location_with_coords(self, lat: float, lon: float):
        """Add location with pre-filled coordinates"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Location from Map")
        dialog.geometry("500x600")
        dialog.configure(bg=self.COLORS['white'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (600 // 2)
        dialog.geometry(f"500x600+{x}+{y}")
        
        tk.Label(dialog,
                text="📍 Add Location from Map",
                font=self.FONTS['title'],
                bg=self.COLORS['white'],
                fg=self.COLORS['primary']).pack(pady=20)
        
        form = tk.Frame(dialog, bg=self.COLORS['white'])
        form.pack(fill='both', expand=True, padx=30)
        
        fields = [
            ('name', "Location Name *"),
            ('latitude', f"Latitude: {lat:.6f}"),
            ('longitude', f"Longitude: {lon:.6f}"),
            ('address', "Address"),
            ('category', "Category"),
            ('description', "Description"),
            ('tags', "Tags (comma-separated)")
        ]
        
        entries = {}
        self._create_form_fields(form, fields, entries, lat=lat, lon=lon)
        
        btn_frame = tk.Frame(dialog, bg=self.COLORS['white'])
        btn_frame.pack(fill='x', padx=30, pady=20)
        
        def save_location():
            try:
                name = entries['name'].get().strip()
                address = entries['address'].get().strip()
                category = entries['category'].get().strip()
                description = entries['description'].get('1.0', tk.END).strip()
                tags = [t.strip() for t in entries['tags'].get().split(',') if t.strip()]
                
                if not name:
                    messagebox.showerror("Error", "Location name is required")
                    return
                
                loc = self.service.add_location(
                    name=name,
                    latitude=lat,
                    longitude=lon,
                    address=address,
                    category=category or "General",
                    description=description,
                    tags=tags
                )
                
                self._load_data()
                self._draw_map()
                dialog.destroy()
                messagebox.showinfo("Success", f"Added location: {loc.name}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add location: {e}")
        
        tk.Button(btn_frame,
                 text="💾 Save Location",
                 font=self.FONTS['body_bold'],
                 bg=self.COLORS['primary'],
                 fg=self.COLORS['white'],
                 relief='flat',
                 padx=30,
                 pady=10,
                 cursor='hand2',
                 command=save_location).pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        tk.Button(btn_frame,
                 text="Cancel",
                 font=self.FONTS['body'],
                 bg=self.COLORS['light'],
                 fg=self.COLORS['dark'],
                 relief='flat',
                 padx=30,
                 pady=10,
                 cursor='hand2',
                 command=dialog.destroy).pack(side='left', fill='x', expand=True, padx=(5, 0))
    
    def _create_form_fields(self, parent, fields, entries, **defaults):
        """Helper to create form fields"""
        for i, (field, label) in enumerate(fields):
            tk.Label(parent,
                    text=label,
                    font=self.FONTS['body_bold'],
                    bg=self.COLORS['white'],
                    fg=self.COLORS['dark']).grid(row=i, column=0, sticky='w', pady=(5, 2))
            
            if field == 'description':
                entry = scrolledtext.ScrolledText(parent,
                                                 height=3,
                                                 font=self.FONTS['body'],
                                                 bg=self.COLORS['light'],
                                                 relief='flat',
                                                 bd=0,
                                                 highlightthickness=1,
                                                 highlightcolor=self.COLORS['primary'])
                entry.grid(row=i, column=1, sticky='ew', pady=(5, 2), padx=(10, 0))
                entries[field] = entry
            elif field in defaults:
                var = tk.StringVar(value=str(defaults[field]))
                entry = tk.Entry(parent,
                                textvariable=var,
                                font=self.FONTS['body'],
                                bg=self.COLORS['light'],
                                relief='flat',
                                bd=0,
                                highlightthickness=1,
                                highlightcolor=self.COLORS['primary'])
                entry.grid(row=i, column=1, sticky='ew', pady=(5, 2), padx=(10, 0))
                entries[field] = var
            else:
                var = tk.StringVar()
                entry = tk.Entry(parent,
                                textvariable=var,
                                font=self.FONTS['body'],
                                bg=self.COLORS['light'],
                                relief='flat',
                                bd=0,
                                highlightthickness=1,
                                highlightcolor=self.COLORS['primary'])
                entry.grid(row=i, column=1, sticky='ew', pady=(5, 2), padx=(10, 0))
                entries[field] = var
        
        parent.grid_columnconfigure(1, weight=1)
    
    # ========================================================================
    # Tracking Methods
    # ========================================================================
    
    def _toggle_tracking(self):
        """Toggle tracking on/off"""
        if not self.is_tracking:
            self._start_tracking()
        else:
            self._stop_tracking()
    
    def _start_tracking(self):
        """Start tracking"""
        self.is_tracking = True
        self.track_points = []
        self.track_btn.config(text="⏹ Stop Tracking", bg=self.COLORS['danger'])
        self.tracking_status.config(text="🔄 Tracking...", fg=self.COLORS['warning'])
        self._set_status("Started tracking")
        
        # Start tracking in background
        self.service.start_tracking(self._update_tracking)
    
    def _stop_tracking(self):
        """Stop tracking"""
        self.is_tracking = False
        self.service.stop_tracking()
        self.track_btn.config(text="▶ Start Tracking", bg=self.COLORS['secondary'])
        self.tracking_status.config(text="⏹️ Stopped", fg=self.COLORS['white'])
        self._set_status("Stopped tracking")
        
        # Save track as route
        if len(self.track_points) > 1:
            route_name = f"Track {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            route = self.service.create_route(route_name, "Auto-tracked route")
            for lat, lon, speed, altitude in self.track_points:
                self.service.add_point_to_route(route.id, lat, lon, speed, altitude)
            self._set_status(f"Saved route with {len(self.track_points)} points")
    
    def _update_tracking(self, lat, lon, speed, altitude):
        """Update tracking display"""
        self.track_points.append((lat, lon, speed, altitude))
        self._draw_map()
        self.tracking_status.config(text=f"📍 {lat:.4f}, {lon:.4f}", fg=self.COLORS['success'])
        
        # Update stats in status
        if len(self.track_points) > 1:
            total_dist = 0
            for i in range(len(self.track_points) - 1):
                p1 = self.track_points[i]
                p2 = self.track_points[i+1]
                dist = self._calculate_distance(p1[0], p1[1], p2[0], p2[1])
                total_dist += dist
            self._set_status(f"Tracking: {len(self.track_points)} points, {total_dist:.2f} km")
    
    def _calculate_distance(self, lat1, lon1, lat2, lon2):
        """Calculate distance between two points in km"""
        R = 6371
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        return R * c
    
    # ========================================================================
    # Demo Data
    # ========================================================================
    
    def _create_demo_locations(self):
        """Create demo locations if none exist"""
        if self.service.get_all_locations():
            return
        
        demo_locations = [
            ("Home", 37.7749, -122.4194, "123 Main St, San Francisco, CA", "Home"),
            ("Work", 37.7858, -122.4002, "456 Market St, San Francisco, CA", "Work"),
            ("Gym", 37.7654, -122.4321, "789 Fitness Ave, San Francisco, CA", "Fitness"),
            ("Coffee Shop", 37.7900, -122.4200, "101 Coffee Ln, San Francisco, CA", "Food"),
            ("Park", 37.7700, -122.4400, "202 Park Blvd, San Francisco, CA", "Outdoor"),
            ("Library", 37.7800, -122.4300, "303 Library St, San Francisco, CA", "Education"),
            ("Hospital", 37.7750, -122.4250, "404 Health Dr, San Francisco, CA", "Medical"),
            ("School", 37.7750, -122.4150, "505 Education Rd, San Francisco, CA", "Education")
        ]
        
        for name, lat, lon, address, category in demo_locations:
            self.service.add_location(
                name=name,
                latitude=lat,
                longitude=lon,
                address=address,
                category=category,
                description=f"Demo location: {name}"
            )
        
        self._load_data()
        self._draw_map()
        self._set_status("Added demo locations")
    
    def _refresh_data(self):
        """Refresh all data"""
        self._load_data()
        self._draw_map()
        self._set_status("Refreshed data")

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point"""
    try:
        root = tk.Tk()
        app = MapTrackerApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()