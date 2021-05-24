# Copyright 2021 AIPlan4EU project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from upf.walkers.dag import DagWalker
import pytamer


class Converter(DagWalker):
    def __init__(self, env, fluents={}, instances={}, parameters={}):
        DagWalker.__init__(self)
        self._env = env
        self._fluents = fluents
        self._instances = instances
        self._parameters = parameters

    def convert(self, expression):
        """Converts the given expression."""
        return self.walk(expression)

    def walk_and(self, expression, args, **kwargs):
        assert len(args) == 2
        return pytamer.tamer_expr_make_and(self._env, args[0], args[1])

    def walk_or(self, expression, args, **kwargs):
        assert len(args) == 2
        return pytamer.tamer_expr_make_or(self._env, args[0], args[1])

    def walk_not(self, expression, args, **kwargs):
        assert len(args) == 1
        return pytamer.tamer_expr_make_not(self._env, args[0])

    def walk_implies(self, expression, args, **kwargs):
        assert len(args) == 2
        return pytamer.tamer_expr_make_implies(self._env, args[0], args[1])

    def walk_iff(self, expression, args, **kwargs):
        assert len(args) == 2
        return pytamer.tamer_expr_make_iff(self._env, args[0], args[1])

    def walk_equals(self, expression, args, **kwargs):
        assert len(args) == 2
        return pytamer.tamer_expr_make_equals(self._env, args[0], args[1])

    def walk_fluent_exp(self, expression, args, **kwargs):
        fluent = expression.fluent()
        ref = pytamer.tamer_expr_make_fluent_reference(self._env, self._fluents[fluent])
        if len(args) == 0:
            return ref
        else:
            return pytamer.tamer_expr_make_functional_apply(self._env, ref, args)

    def walk_bool_constant(self, expression, args, **kwargs):
        assert len(args) == 0
        if expression.is_true():
            return pytamer.tamer_expr_make_true(self._env)
        else:
            return pytamer.tamer_expr_make_false(self._env)

    def walk_param_exp(self, expression, args, **kwargs):
        assert len(args) == 0
        p = expression.parameter()
        return pytamer.tamer_expr_make_parameter_reference(self._env, self._parameters[p])

    def walk_object_exp(self, expression, args, **kwargs):
        assert len(args) == 0
        o = expression.object()
        return pytamer.tamer_expr_make_instance_reference(self._env, self._instances[o])
