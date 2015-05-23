from django.conf.urls import include, url
from django.conf import settings
from django.shortcuts import render

from mapit.views import areas, postcodes

handler500 = 'mapit.shortcuts.json_500'

format_end = '(?:\.(?P<format>html|json))?'
area_id = '(?P<area_id>[0-9A-Za-z:]+)'

urlpatterns = [
    url(r'^$', render, {'template_name': 'mapit/index.html'}, 'mapit_index'),
    url(r'^licensing$', render, {'template_name': 'mapit/licensing.html'}),
    url(r'^overview$', render, {'template_name': 'mapit/overview.html'}),

    url(r'^generations%s$' % format_end, areas.generations, {}, 'mapit_generations'),

    url(r'^postcode/$', postcodes.form_submitted),
    url(r'^postcode/(?P<postcode>[A-Za-z0-9 +]+)%s$' % format_end, postcodes.postcode, name="mapit-postcode"),
    url(r'^postcode/partial/(?P<postcode>[A-Za-z0-9 ]+)%s$' % format_end,
        postcodes.partial_postcode, name="mapit-postcode-partial"),

    url(r'^area/%s%s$' % (area_id, format_end), areas.area),
    url(r'^area/%s\.(?P<format>kml|geojson|wkt)$' % area_id, areas.area_polygon), areas.area_polygon),
    url(r'^area/(?P<srid>[0-9]+)/%s\.(?P<format>kml|json|geojson|wkt)$' % area_id,
    url(r'^area/%s/example_postcode%s$' % (area_id, format_end), postcodes.example_postcode_for_area),
    url(r'^area/%s/children%s$' % (area_id, format_end), areas.area_children),
    url(r'^area/%s/geometry$' % area_id, areas.area_geometry),
    url(r'^area/%s/touches%s$' % (area_id, format_end), areas.area_touches),
    url(r'^area/%s/overlaps%s$' % (area_id, format_end), areas.area_overlaps),
    url(r'^area/%s/covers%s$' % (area_id, format_end), areas.area_covers),
    url(r'^area/%s/covered%s$' % (area_id, format_end), areas.area_covered),
    url(r'^area/%s/coverlaps%s$' % (area_id, format_end), areas.area_coverlaps),
    url(r'^area/%s/intersects%s$' % (area_id, format_end), areas.area_intersects),

    url(r'^point/$', areas.point_form_submitted),
    url(r'^point/(?P<srid>[0-9]+)/(?P<x>[0-9.-]+),(?P<y>[0-9.-]+)(?:/(?P<bb>box))?%s$' % format_end,
        areas.areas_by_point),
    url(r'^point/latlon/(?P<lat>[0-9.-]+),(?P<lon>[0-9.-]+)(?:/(?P<bb>box))?%s$' % format_end,
        areas.areas_by_point_latlon),
    url(r'^point/osgb/(?P<e>[0-9.-]+),(?P<n>[0-9.-]+)(?:/(?P<bb>box))?%s$' % format_end,
        areas.areas_by_point_osgb),

    url(r'^nearest/(?P<srid>[0-9]+)/(?P<x>[0-9.-]+),(?P<y>[0-9.-]+)%s$' % format_end, postcodes.nearest),

    url(r'^areas/(?P<area_ids>[0-9A-Za-z:]+(?:,[0-9A-Za-z:]+)*)%s$' % format_end, areas.areas),
    url(r'^areas/(?P<area_ids>[0-9A-Za-z:]+(?:,[0-9A-Za-z:]+)*)/geometry$', areas.areas_geometry),
    url(r'^areas/(?P<type>[A-Z0-9,]*[A-Z0-9]+)%s$' % format_end, areas.areas_by_type),
    url(r'^areas/(?P<name>.+?)%s$' % format_end, areas.areas_by_name),
    url(r'^areas$', areas.deal_with_POST, {'call': 'areas'}),
    url(r'^code/(?P<code_type>[^/]+)/(?P<code_value>[^/]+?)%s$' % format_end, areas.area_from_code),
]

# Include app-specific urls
if (settings.MAPIT_COUNTRY == 'GB'):
    urlpatterns.append(
        url(r'^', include('mapit_gb.urls')),
    )
