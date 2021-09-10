import sbol3
import tyto


def has_vector_role(component: sbol3.Component) -> bool:
    """Check if a Component has a vector role (i.e., is a plasmid or similar)

    :param component: SBOL3 component to check
    :return: true if the component is a vector
    """
    return any(r for r in component.roles
               if tyto.SO.plasmid.is_ancestor_of(r) or tyto.SO.vector_replicon.is_ancestor_of(r))


def vector_to_insert(component: sbol3.Component) -> sbol3.Component:
    """If the component is a vector, peel it open to find the sub-component that is not the vector portion
    If the component is not a vector, return it directly
    Throws a ValueError if the component is a vector but does not have precisely one insert

    :param component: SBOL3 component to extract from
    :return: component if not vector; otherwise the vector
    """
    # is either the component or any feature thereof a vector? If not, then return component
    subvectors = {f for f in component.features
                  if isinstance(f, sbol3.SubComponent) and has_vector_role(f.instance_of.lookup()) }
    if len(subvectors) == 0 and not has_vector_role(component):
        return component
    # otherwise, if there's precisely one non-vector subcomponent, return the Component it points to
    inserts = {f for f in set(component.features)-subvectors if isinstance(f, sbol3.SubComponent)}
    if len(inserts) == 1:
        return inserts.pop().instance_of.lookup()
    else:
        raise ValueError(f'Vector should have one insert, but found {len(inserts)}: {component.identity}')