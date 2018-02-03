import plyj.parser as plyj
import plyj.model as m

parser = plyj.Parser()
file = open(r'C:\personal-git\apache\commons-math\src\test\java\org\apache\commons\math4\optim\nonlinear\scalar\noderiv\BOBYQAOptimizerTest.java')
tree = parser.parse_file(file)
print('declared types:')
for type_decl in tree.type_declarations:
    method_annotations_tuples = []
    print('methods:')
    for method_decl in [decl for decl in type_decl.body if type(decl) is m.MethodDeclaration]:
        annotations = []
        for modifier in method_decl.modifiers:
            if type(modifier) is m.Annotation:
                annotations.append(modifier.name.value)
        method_annotations_tuples.append((method_decl.name, annotations))
a=5
