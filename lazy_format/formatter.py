# coding=utf-8
import string


class LazyFormatter(string.Formatter):
    def _unsplit_var(self, conversion, field_name, format_spec):
        variable = (
            '{',
            field_name,
            (('!' + conversion) if conversion else ''),
            ((':' + format_spec) if format_spec else ''),
            '}'
        )
        return ''.join(variable)

    def _vformat(self, format_string, args, kwargs, used_args, recursion_depth):
        if recursion_depth < 0:
            raise ValueError('Max string recursion exceeded')
        result = []
        for literal_text, field_name, format_spec, conversion in \
                self.parse(format_string):

            if literal_text:
                result.append(literal_text)

            if field_name is not None:
                try:
                    obj, arg_used = self.get_field(field_name, args, kwargs)
                    used_args.add(arg_used)
                    format_spec = self._vformat(format_spec, args, kwargs,
                                                used_args, recursion_depth - 1)
                    rendered = self.format_field(self.convert_field(obj, conversion), format_spec)
                except (KeyError, IndexError):
                    format_spec = self._vformat(format_spec, args, kwargs,
                                                used_args, recursion_depth - 1)
                    rendered = self._unsplit_var(conversion, field_name, format_spec)

                result.append(rendered)

        return ''.join(result)


__all__ = ['LazyFormatter']