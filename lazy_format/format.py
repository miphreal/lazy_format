import string


class LazyFormatter(string.Formatter):

    def _unsplit_var(self, field_name, format_spec, conversion):
        variable = (
            '{',
            field_name,
            (('!' + conversion) if conversion else ''),
            ((':' + format_spec) if format_spec else ''),
            '}'
        )
        return ''.join(variable)

    def _vformat(self, format_string, args, kwargs, used_args, recursion_depth,
                 auto_arg_index=0):
        if recursion_depth < 0:
            raise ValueError('Max string recursion exceeded')
        result = []
        for literal_text, field_name, format_spec, conversion in \
                self.parse(format_string):

            # output the literal text
            if literal_text:
                result.append(literal_text)

            # if there's a field, output it
            if field_name is not None:
                # this is some markup, find the object and do
                #  the formatting

                # handle arg indexing when empty field_names are given.
                if field_name == '':
                    if auto_arg_index is False:
                        raise ValueError('cannot switch from manual field '
                                         'specification to automatic field '
                                         'numbering')
                    field_name = str(auto_arg_index)
                    auto_arg_index += 1
                elif field_name.isdigit():
                    if auto_arg_index:
                        raise ValueError('cannot switch from manual field '
                                         'specification to automatic field '
                                         'numbering')
                    # disable auto arg incrementing, if it gets
                    # used later on, then an exception will be raised
                    auto_arg_index = False

                try:
                    # given the field_name, find the object it references
                    #  and the argument it came from
                    obj, arg_used = self.get_field(field_name, args, kwargs)
                    used_args.add(arg_used)

                except (KeyError, IndexError):
                    format_spec, auto_arg_index = self._vformat(
                        format_spec, args, kwargs,
                        used_args, recursion_depth-1,
                        auto_arg_index=auto_arg_index)

                    result.append(self._unsplit_var(
                        field_name, format_spec, conversion
                    ))

                else:
                    # do any conversion on the resulting object
                    obj = self.convert_field(obj, conversion)

                    # expand the format spec, if needed
                    format_spec, auto_arg_index = self._vformat(
                        format_spec, args, kwargs,
                        used_args, recursion_depth-1,
                        auto_arg_index=auto_arg_index)

                    # format the object and append to the result
                    result.append(self.format_field(obj, format_spec))

        return ''.join(result), auto_arg_index


class LazyFormat:

    _formatter = LazyFormatter()

    def __init__(self, text, *args, **kwargs):
        self._text = text
        self._format_args = args
        self._format_kwargs = kwargs

    def format(self, *args, **kwargs):
        format_args = self._format_args + args
        format_kwargs = dict(self._format_kwargs, **kwargs)
        formatted_text = self._formatter.vformat(self._text, format_args, format_kwargs)
        return LazyFormat(formatted_text, *format_args, **format_kwargs)

    __format__ = format

    def __str__(self):
        return str(self._text)

    def __repr__(self):
        return repr(self._text)

    def __eq__(self, other):
        if isinstance(other, (str, LazyFormat)):
            return str(self._text) == str(other)

        return NotImplemented

    def __len__(self):
        return len(self._text)
