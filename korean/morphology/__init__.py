# -*- coding: utf-8 -*-
"""
    korean.morphology
    ~~~~~~~~~~~~~~~~~

    :copyright: (c) 2012 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

import sys
import types


__all__ = 'Morphology', 'Morpheme', 'Particle', 'Substantive', 'Noun', \
          'NumberWord', 'allomorph', 'define_allomorphic_variation',


class Morphology(object):

    _registry = {}

    @classmethod
    def _register_morpheme(cls, morpheme_cls):
        for attr in dir(morpheme_cls):
            if not attr.startswith('$'):
                continue
            for keyword, func in getattr(morpheme_cls, attr):
                keyword = (morpheme_cls,) + keyword
                if keyword in cls._registry:
                    raise ValueError('Already defined inflection rule')
                try:
                    cls._registry[attr][keyword] = func
                except KeyError:
                    cls._registry[attr] = {keyword: func}

    @classmethod
    def _make_decorator(cls, tmp_attr, keyword):
        assert tmp_attr.startswith('$')
        frm = sys._getframe(2)
        def decorator(func):
            rule = (keyword, func)
            try:
                frm.f_locals[tmp_attr].append(rule)
            except KeyError:
                frm.f_locals[tmp_attr] = [rule]
            return func
        return decorator

    @classmethod
    def define_allomorphic_variation(cls, prefix_of=None, suffix_of=None):
        if not (prefix_of or suffix_of):
            raise TypeError('prefix_of or suffix_of should be defined')
        elif bool(prefix_of) == bool(suffix_of):
            raise TypeError('Cannot specify prefix_of and suffix_of both')
        keyword = (prefix_of, suffix_of)
        return cls._make_decorator('$allomorphic_variations', keyword)

    @classmethod
    def allomorph(cls, morpheme, prefix_of=None, suffix_of=None):
        prefix_type = prefix_of and type(prefix_of)
        suffix_type = suffix_of and type(suffix_of)
        key = (type(morpheme), prefix_type, suffix_type)
        func = cls._registry['$allomorphic_variations'][key]
        bound_func = types.MethodType(func, morpheme)
        return bound_func(prefix_of or suffix_of)


allomorph = Morphology.allomorph
define_allomorphic_variation = Morphology.define_allomorphic_variation
#merge = Morphology.merge


#: Imports submodules on the end. Because they might need :class:`Morphology`.
from .morpheme import Morpheme
from .particle import Particle
from .substantive import Substantive, Noun, NumberWord
