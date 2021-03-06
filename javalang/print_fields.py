#!/usr/bin/env python2

import ParserExceptions
import javalang
import sys


def parse_file():
    with open(sys.argv[1], 'r') as java_file:
        file_contents = java_file.read()
    tree = javalang.parse.parse(file_contents)
    if len(tree.types) is 0:
        raise ParserExceptions.ClassNotFoundException('Unable to find Java class in ' + sys.argv[1])
    return tree


def get_class_signature(class_declaration):
    class_signature = class_declaration.name
    if class_declaration.extends is not None:
        class_signature += ' extends ' + class_declaration.extends.name
    if class_declaration.implements is not None:
        class_signature += ' implements ' + ', '.join([interface.name for interface in class_declaration.implements])
    return class_signature


def reconstruct_argument(argument_piece):
    if argument_piece.__class__.__name__ is 'Literal':
        return argument_piece.value[1:-1]  #strip opening and closing double quotes
    elif argument_piece.__class__.__name__ is not 'BinaryOperation':
        raise ParserExceptions.UnsupportedAnnotationOperationException('UNSUPPORTED ANNOTATION OPERATION: '
                                                                       + argument_piece.__class__.__name__)
    else:
        return reconstruct_argument(argument_piece.operandl) + reconstruct_argument(argument_piece.operandr)


def get_annotation_argument(children):
    if children[1] is None:
        return ''
    else:
        return '("' + reconstruct_argument(children[1]) + '")'  # children[1] is the first argument


def get_annotation_string(annotation):
    return annotation.name + get_annotation_argument(annotation.children)


def get_field_string(field_declaration):
    field_string = ' '.join([modifier for modifier in field_declaration.modifiers]) + ' '
    field_string += field_declaration.type.name + ' ' + field_declaration.declarators[0].name
    return field_string


def main():
    # Parse the Java file
    tree = parse_file()

    # Get class information
    class_declaration = tree.types[0]

    # Print class information
    print(get_class_signature(class_declaration))
    print

    # Print fields
    for field_declaration in class_declaration.fields:
        for annotation in field_declaration.annotations:
            print('\t@' + get_annotation_string(annotation))
        print('\t' + get_field_string(field_declaration))
        print

if __name__ == "__main__":
    main()