# -*- coding: utf-8 -*-

import os
import Image

from django.forms.util import flatatt
from django.forms.widgets import Input
from django.utils.datastructures import MultiValueDict, MergeDict
from django.utils.encoding import force_unicode
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe



class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None):
        output = []
        if value and getattr(value, "url", None):

            image_url = value.url
            file_name = str(value)

            # defining the size
            size = '300x300'
            x, y = [int(x) for x in size.split('x')]

            # defining the filename and the miniature filename
            filehead, filetail = os.path.split(value.path)
            basename, format = os.path.splitext(filetail)
            miniature = basename + '_' + size + format
            filename = value.path
            miniature_filename = os.path.join(filehead, miniature)
            filehead, filetail = os.path.split(value.url)
            miniature_url = filehead + '/' + miniature

            # make sure that the thumbnail is a version of the current original sized image
            if os.path.exists(miniature_filename) and os.path.getmtime(filename) > os.path.getmtime(miniature_filename):
                os.unlink(miniature_filename)

            # if the image wasn't already resized, resize it
            if not os.path.exists(miniature_filename):
                image = Image.open(filename)
                image.thumbnail([x, y], Image.ANTIALIAS)
                try:
                    image.save(miniature_filename, image.format, quality=100, optimize=1)
                except:
                    image.save(miniature_filename, image.format, quality=100)

            output.append(u' <div><a href="%s" target="_blank"><img src="%s" alt="%s" /></a></div> %s ' % \
                          (miniature_url, miniature_url, miniature_filename, _('&nbsp;')))

        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))


class MultipleInput(Input):
    input_type = 'text'

    def __init__(self, attrs=None, choices=()):
        super(MultipleInput, self).__init__(attrs)
        self.choices = choices

    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        id_ = final_attrs.get('id', None)
        inputs = []
        for i, v in enumerate(value):
            input_attrs = dict(value=force_unicode(v), **final_attrs)
            if id_:
                input_attrs['id'] = '%s_%s' % (id_, i)
            inputs.append(u'<p><input%s /><a href="#" id="remove_%s">Remove</a></p>' % (flatatt(input_attrs), id_))
        return mark_safe(u'\n'.join(inputs))

    def value_from_datadict(self, data, files, name):
        if isinstance(data, (MultiValueDict, MergeDict)):
            return data.getlist(name)
        return data.get(name, None)